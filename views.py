import logging
from django.contrib import messages
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from motorfleet.models import Vehicle, Claim
from motorfleet.forms import FleetForm, MotorfleetProfileForm, VehicleFormSet, ClaimFormSet, ConvictionFormSet
from groupmanager.forms import AddressForm


@login_required
def fleet(request, fleet_id):

    if request.method == 'POST':     
        messages.error(request, 'not handling posts yet')
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    else:  
        if fleet_id != '0':
            mf = get_object_or_404(Motorfleet, pk=fleet_id)
            mf_form = FleetForm(instance=mf)
        else:
            mf_form = FleetForm()
            return render_to_response('motorfleet/editmotorfleet.html', {'sharedexpense': se, 'participants':participants, 'is_org': is_org },context_instance=RequestContext(request))

    if se.is_participant(request.user):
        logging.info("WSA: user %s is a participant of fleet %s." % (request.user.username, fleet_id))
        is_org = False
    elif se.is_organiser(request.user):
        logging.info("WSA: user %s is the organiser of sharedexpense %s." % (request.user.username, fleet_id))
        is_org = True
    else:
        logging.info("WSA: user %s does not have permission to view this sharedexpense %s" % (request.user.username, fleet_id))
        messages.error(request, 'Sorry you do not have permission to see that shareable, if you think you should please let us know.')
        return redirect('web-welcome')

    participants = []
    participants.append(se.get_organiser())
    participants.extend(list(se.get_participants()))
    logging.debug("WSA: participants %s of sharedexpense %s" % (participants, sharedexpense_id))

    return render_to_response('motorfleet/motorfleet.html', {'sharedexpense': se, 'participants':participants, 'is_org': is_org },context_instance=RequestContext(request))

@login_required
def editfleet(request, fleet_id):

    if request.method == 'POST':     
        if fleet_id == '0': #if 0 we are creating a new one not editing and existing one
            mf_form = FleetForm(request.POST)
        else:
            mf = get_object_or_404(Fleet, pk=fleet_id)
            mf_form = FleetForm(request.POST, instance=mf)
        if  mf_form.is_valid():
            mf = mf_form.save(commit=False)
            if fleet_id == '0':
                group = Group(name=mf.name, organiser=request.user)
                group.save()	
                mf.group_id = group.id
            mf.save()
            return HttpResponseRedirect(str(settings.DOMAIN_ROOT_URL) + '/motorfleet/' + str(mf.id) + '/')
        else:
            #TODO: find out why and tell them
            messages.error(request, 'Your fleet creation failed because: %s. If you think this error should not have occurred please let us know.' % str(mf_form.errors))
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
    else:  
        if fleet_id != '0': #if 0 we are creating a new one not editing and existing one
            mf = get_object_or_404(Fleet, pk=fleet_id)
            mf_form = FleetForm(instance=mf)
        else:
            mf = ''
            mf_form = FleetForm()
        return render_to_response("motorfleet/edit_motorfleet.html",{'mf': mf, 'mf_form':mf_form },context_instance=RequestContext(request))



@login_required
def personaldetails(request, user_id):
    if request.method == 'POST':     
        messages.error(request, 'not handling posts yet')
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    else:  
        if user_id != '0':
            u = get_object_or_404(User, pk=user_id)
            profile_form = MotorfleetProfileForm(instance=u.motorfleet_profile)
            address_form = AddressForm(instance=u.address)
        else:
            profile_form = MotorfleetProfileForm()
            address_form = AddressForm()

    return render_to_response("motorfleet/edit_personaldetails.html",{'profile_form':profile_form, 'address_form':address_form },context_instance=RequestContext(request))


@login_required
def drivinghistory(request, user_id):
    if request.method == 'POST':     
        messages.error(request, 'not handling posts yet')
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    else:  
        if user_id != '0':
            u = get_object_or_404(User, pk=user_id)
            claims_formset = ClaimFormSet(queryset=Claim.objects.all().filter(claimant=u))
            convictions_formset = ConvictionFormSet(queryset=Conviction.objects.all().filter(convicted=u))
        else:
            claims_formset = ClaimFormSet()
            convictions_formset = ConvictionFormSet()
            logging.debug("WSA: convictions_formset %s" % str(convictions_formset))
    return render_to_response("motorfleet/edit_drivinghistory.html",{'claims_formset':claims_formset, 'convictions_formset':convictions_formset },context_instance=RequestContext(request))


@login_required
def addvehicles(request, sharedexpense_id, user_id):

    if request.method == 'POST':
        se = get_object_or_404(SharedExpense, pk=sharedexpense_id)
        if se.is_participant(request.user) or  se.is_organiser(request.user):
            user = get_object_or_404(User, pk=user_id)
            vehicle_formset = VehicleFormSet(request.POST, prefix=user_id)
            logging.debug("WSA: Vehicle Form %s" % str(vehicle_formset))
            if vehicle_formset.is_valid():
                vehicles = vehicle_formset.save(commit=False)
                for vehicle in vehicles:
                    #add in the mandatory fields not collected on form
                    vehicle.owner = user
                    vehicle.save()
                    logging.info("WSA: Added vehicle %s to user %s" % (vehicle.make, user.first_name))
            else:
                logging.info("WSA: Failed to add new Vehicle to User %s with error %s" % (user.first_name, str(vehicle_formset.errors)))
                messages.error(request, 'Your vehicle update failed because: %s. If you think this error should not have occurred please let us know.' % str(vehicle_formset.errors))

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def addclaims(request, sharedexpense_id, user_id):

    if request.method == 'POST':
        se = get_object_or_404(SharedExpense, pk=sharedexpense_id)
        if se.is_participant(request.user) or  se.is_organiser(request.user):
            user = get_object_or_404(User, pk=user_id)
            claim_formset = ClaimFormSet(request.POST, prefix=user_id)
            logging.debug("WSA: Claim Form %s" % str(claim_formset))
            if claim_formset.is_valid():
                claims = claim_formset.save(commit=False)
                for claim in claims:
                    #add in the mandatory fields not collected on form
                    claim.driver = user
                    claim.save()
                    logging.info("WSA: Added claim for %s to user %s" % (claim.amount, user.first_name))
            else:
                logging.info("WSA: Failed to add new Claim to User %s with error %s" % (user.first_name, str(claim_formset.errors)))
                messages.error(request, 'Your claim update failed because: %s. If you think this error should not have occurred please let us know.' % str(claim_formset.errors))

    return HttpResponseRedirect(request.META['HTTP_REFERER'])
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomerForm, TractorForm, ImplementForm
from .models import customer, tractor_details, implements, ownership_history

def customer_list(request):
    customers = customer.objects.all()
    return render(request, 'tracker/customer_list.html', {'customers': customers})

def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm()
    return render(request, 'tracker/customer_form.html', {'form': form})

def tractor_list(request):
    tractors = tractor_details.objects.all()
    return render(request, 'tracker/tractor_list.html', {'tractors': tractors})

def tractor_create(request):
    if request.method == 'POST':
        form = TractorForm(request.POST)
        if form.is_valid():
            tractor = form.save(commit=False)
            tractor.updated_by = request.user
            tractor.save()
            return redirect('tractor_list')
    else:
        form = TractorForm()
    return render(request, 'tracker/tractor_form.html', {'form': form})

def implement_list(request):
    implement = implements.objects.all()
    return render(request, 'tracker/implement_list.html', {'implement': implement})

def implement_create(request):
    if request.method == 'POST':
        form = ImplementForm(request.POST)
        if form.is_valid():
            implement = form.save(commit=False)
            implement.updated_by = request.user
            implement.save()
            return redirect('implement_list')
    else:
        form = ImplementForm()
    return render(request, 'tracker/implement_form.html', {'form': form})

def tractor_update(request, pk):
    tractor = get_object_or_404(tractor_details, pk=pk)
    if request.method == 'POST':
        form = TractorForm(request.POST, instance=tractor)
        if form.is_valid():
            old_owner = tractor.owner
            new_tractor = form.save(commit=False)
            new_tractor.updated_by = request.user
            new_tractor.save()
            if old_owner != new_tractor.owner:
                ownership_history.objects.create(
                    tractor=new_tractor,
                    previous_owner=old_owner,
                    new_owner=new_tractor.owner,
                    updated_by=request.user
                )
            return redirect('tractor_list')
    else:
        form = TractorForm(instance=tractor)
    return render(request, 'tracker/tractor_form.html', {'form': form})

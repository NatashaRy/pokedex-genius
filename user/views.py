from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


@login_required
def change_email(request):
    if request.method == 'POST':
        form = EmailUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            # Redirect to a success page or show a success message
            return redirect('#')
    else:
        form = EmailUpdateForm(instance=request.user)

    return render(request, 'email_change.html', {'form': form})

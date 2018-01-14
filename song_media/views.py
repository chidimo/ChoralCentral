"""views"""

from django.views import generic, View
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django_addanother.views import CreatePopupMixin

from .models import Sheet, Midi, VideoLink
from .forms import NewSheetForm, NewMidiForm, NewVideoLinkForm

from siteuser.models import SiteUser

class SheetAdd(LoginRequiredMixin, generic.CreateView):
    template_name = 'song_media/sheet_new.html'
    form_class = NewSheetForm

    def form_valid(self, form):
        form.instance.uploader = SiteUser.objects.get(user=self.request.user)
        self.object = form.save()
        self.object.likes.add(SiteUser.objects.get(user=self.request.user))
        return redirect(self.get_success_url())

    def get_form_kwargs(self):
        """include 'user' and 'pk' in the kwargs to be sent to form"""
        kwargs = super(SheetAdd, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['pk'] = self.kwargs.get('pk', None)
        return kwargs

class DisplaySheet(View):
    def get(self, request, *args, **kwargs):
        pdf = get_object_or_404(Sheet, pk=self.kwargs.get('pk', None))
        fname = os.path.basename(pdf.file.url)
        path = os.path.join(settings.MEDIA_ROOT, 'sheets\\' + fname)
        response = FileResponse(open(path, 'rb'), content_type="application/pdf")
        response["Content-Disposition"] = "filename={}_{}".format(pdf.part, fname)
        return response

class MidiAdd(LoginRequiredMixin, generic.CreateView):
    model = Midi
    template_name = 'song_media/midi_new.html'
    form_class = NewMidiForm

    # def form_valid(self, form): implement likes first
    #     form.instance.uploader = SiteUser.objects.get(user=self.request.user)
    #     self.object = form.save()
    #     self.object.likes.add(SiteUser.objects.get(user=self.request.user))
    #     return redirect(self.get_success_url())

    def form_valid(self, form):
        form.instance.uploader = SiteUser.objects.get(user=self.request.user)
        return super(MidiAdd, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(MidiAdd, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['pk'] = self.kwargs.get('pk', None)
        return kwargs

class PlayMidi(View):
    def get(self, request, *args, **kwargs):
        midi = get_object_or_404(Midi, pk=self.kwargs.get('pk', None))
        fname = os.path.basename(midi.file.url)
        path = os.path.join(settings.MEDIA_ROOT, 'midi\\' + fname)
        response = FileResponse(open(path, 'rb'), content_type="audio/midi")
        response["Content-Disposition"] = "filename={}_{}".format(midi.part, fname)
        return response

class VideoLinkAdd(LoginRequiredMixin, generic.CreateView):
    model = VideoLink
    template_name = 'song_media/videolink_new.html'
    form_class = NewVideoLinkForm

    def form_valid(self, form):
        form.instance.uploader = SiteUser.objects.get(user=self.request.user)
        return super(VideoLinkAdd, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(VideoLinkAdd, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['pk'] = self.kwargs.get('pk', None)
        return kwargs

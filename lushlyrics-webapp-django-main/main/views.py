from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import playlist_user
from django.urls.base import reverse
from django.contrib.auth import authenticate, login as auth_login, logout 
from youtube_search import YoutubeSearch
from django.contrib.auth.decorators import login_required
import json
# import cardupdate


def login_view(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        auth_login(request, user)
        return redirect('default')
    else:
        return render(request, 'login.html', {'case': False})
  return render(request, 'login.html')

def signup(request):
  if request.method == 'POST':
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    confirm_password = request.POST['confirm-password']

    if password != confirm_password:
      return render(request, 'signup.html', {'error': 'Passwords do not match'})

    if User.objects.filter(username=username).exists():
      return render(request, 'signup.html', {'error': 'Username already exists'})

    if User.objects.filter(email=email).exists():
      return render(request, 'signup.html', {'error': 'Email already exists'})

    user = User.objects.create_user(username, email, password)
    user.save()
    auth_login(request, user)
    return redirect('default')
  return render(request, 'signup.html')

def logout_view(request):
  logout(request)
  return redirect('login')


f = open('card.json', 'r')
CONTAINER = json.load(f)

def default(request):
  if not request.user.is_authenticated:
    return redirect('login')

  global CONTAINER
  if request.method == 'POST':
    add_playlist(request)
    return HttpResponse("")

  song = 'kSFJGEHDCrQ'
  return render(request, 'player.html',{'CONTAINER':CONTAINER, 'song':song})


def playlist(request):
    if not request.user.is_authenticated:
      return redirect('login')
    cur_user = playlist_user.objects.get(username = request.user)
    try:
      song = request.GET.get('song')
      song = cur_user.playlist_song_set.get(song_title=song)
      song.delete()
    except:
      pass
    if request.method == 'POST':
        add_playlist(request)
        return HttpResponse("")
    song = 'kSFJGEHDCrQ'
    user_playlist = cur_user.playlist_song_set.all()
    # print(list(playlist_row)[0].song_title)
    return render(request, 'playlist.html', {'song':song,'user_playlist':user_playlist})


def search(request):
  if request.method == 'POST':

    add_playlist(request)
    return HttpResponse("")
  try:
    search = request.GET.get('search')
    song = YoutubeSearch(search, max_results=10).to_dict()
    song_li = [song[:10:2],song[1:10:2]]
    # print(song_li)
  except:
    return redirect('/')

  return render(request, 'search.html', {'CONTAINER': song_li, 'song':song_li[0][0]['id']})


def add_playlist(request):
    cur_user = playlist_user.objects.get(username = request.user)

    if (request.POST['title'],) not in cur_user.playlist_song_set.values_list('song_title', ):

        songdic = (YoutubeSearch(request.POST['title'], max_results=1).to_dict())[0]
        song__albumsrc=songdic['thumbnails'][0]
        cur_user.playlist_song_set.create(song_title=request.POST['title'],song_dur=request.POST['duration'],
        song_albumsrc = song__albumsrc,
        song_channel=request.POST['channel'], song_date_added=request.POST['date'],song_youtube_id=request.POST['songid'])
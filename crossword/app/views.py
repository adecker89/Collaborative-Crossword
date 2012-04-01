from django.core.context_processors import csrf
from django.shortcuts import render

from django_socketio import events

from puzReader import puzFormat

def home(request):
    print "home"
    puz = puzFormat()
    puz.read('jz120105.puz')
    
    c = {'puz':puz,'ys':range(puz.height),'xs':range(puz.width),'board':puz.board}
    c.update(csrf(request))
    return render(request, 'crossword.html', c)


from django.http import HttpResponse, Http404
from django.template import Context
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json

from quizer.forms import *
from quizer.models import *

def main_page(request):
	context = {
		'user': request.user,
	}
	return render(request, 'main_page.html', context)
	
def get_score(request, quiz_id):
	try:
		user = request.user
		quiz = user.quiz_set.get(id=quiz_id)
		scores = quiz.score_set.all()
				
	except:
		raise Http404('You did not provide answer for question %s ' %question.question_text)
	context = {
		'user': request.user,
		'quiz': quiz,
		'scores': scores, 
	}
	return render(request, 'quiz_scores.html', context)


@csrf_exempt
def set_date(request, quiz_id):
	try:
		user = request.user
		quiz = Quiz.objects.get(id=quiz_id)
		
		if request.method == "POST" and request.is_ajax():
			start = request.POST['start']
			end = request.POST['end']
			print(start)
			print(end)
	
		quiz_score, created = Score.objects.get_or_create(
			user = user,
			quiz = quiz,
			score = 0,
			start_time = start,
			end_time = end,
		)
		quiz_score.save();	
	except:
		raise Http404('You did not provide answer for some questions')
	
	
def score(request, quiz_id):
	try:
		user = request.user
		quiz = Quiz.objects.get(id=quiz_id)
		questions = quiz.question_set.all()
		sval = 0
		found = 0
		
		if request.method == "POST":
			for question in questions:
				selected_choice = request.POST['choice'+str(question.id)]
				if int(selected_choice) == int(question.answer) :
					sval = sval+1

		for user_scores in user.score_set.all():	
			if user_scores.quiz.title == quiz.title:
				user_scores.score = sval
				user_scores.save()
				found = 1
		
		
	except:
		raise Http404('You did not provide answer for some questions')
	context = {
		'user': request.user,
		'quiz': quiz,
		'questions': questions, 
		'score': sval,
		'total': len(questions),
	}
	return render(request, 'quiz.html', context)
	
def quiz(request, quiz_id):
	try:
		user = request.user
		quiz = Quiz.objects.get(id=quiz_id)
		questions = quiz.question_set.all()
		start_time = '1'
		end_time = '1'
		
		for user_scores in user.score_set.all():	
			if user_scores.quiz.title == quiz.title:
				if user_scores.start_time != '1':
					start_time = user_scores.start_time;
					end_time = user_scores.end_time;
		
	except:
		raise Http404('Requested user not found.')
	context = {
		'user': user,
		'quiz': quiz,
		'jquiz': json.dumps(quiz.id),
		'questions': questions,
		'start_time': json.dumps(start_time),
		'end_time': json.dumps(end_time), 
	}
	
	if user == quiz.user :
		return render(request, 'quiz_edit.html', context)
	else :
		return render(request, 'quiz.html', context)

def user_page(request):
	try:
		user = request.user
		quizzes = user.quiz_set.all()
	except:
		raise Http404('Requested user not found.')
	context = {
		'user': request.user,
		'quizzes': quizzes,
		
	}
	return render(request, 'user_page.html', context)
	

def logout_page(request):
	logout(request)
	return HttpResponseRedirect('/main_page.html')
	

def register_page(request):
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			user = User.objects.create_user(
			username=form.cleaned_data['username'],
			password=form.cleaned_data['password1'],
			email=form.cleaned_data['email']
			)
			return render(request, 'registration/register_success.html')
	else:
		form = RegistrationForm()
		context = {
			'form': form
		}
		
	return render(request, 'registration/register.html', context)
	
def register_success_page(request):
	return render(request, 'registration/register_success.html')
	
@login_required
def question_save_page(request):
	if request.method == 'POST':
		form = QuizSaveForm(request.POST)
		if form.is_valid():
		
			# Create or get quiz.
			quiz, created = Quiz.objects.get_or_create(
				user = request.user,
				title = form.cleaned_data['title'],
				time = form.cleaned_data['time']
			)
			quiz.save()
			# Create or get question.
			question, created = Question.objects.get_or_create(
				quiz = quiz,
				question_text = form.cleaned_data['question'],
				answer = form.cleaned_data['answer'],
			)
			question.save()
			
			
			# Create or get quiz.
			for i in range(1,5):
				chstr = "choice"+str(i)
				choice, created = Choice.objects.get_or_create(
					question = question,
					choice_text = form.cleaned_data[chstr],
				)
				choice.save()
			
			
			
			return HttpResponseRedirect(
				'/user/'
			)
	else:
		form = QuizSaveForm()	
	return render(request, 'quiz.html', {'form': form})
	

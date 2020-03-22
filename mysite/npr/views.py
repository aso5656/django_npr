from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.views import generic
from django.shortcuts import redirect,reverse,render
from django.db.models import Q #多条件查询
from django.http import Http404
from .functions import *
from .models import *
from django.utils import timezone
from multiprocessing import Pool,freeze_support
from functools import wraps

# Create your views here.
if __name__ == '__main__':
    freeze_support()

class IndexView(generic.ListView):
    template_name='npr/index.html'
    model = Podcast
    
    def get_context_data(self,**kwargs):
        context = super(IndexView,self).get_context_data(**kwargs)
        context['category'] = Category.objects.all()

        order = self.kwargs.get('order') #catch order 
        if order:
            if order=='by_name':
                context['podcast'] = Podcast.objects.all().order_by('title')
            elif order =='by_date':
                context['order'] = 'by_date'
                context['podcast'] = sorted(Podcast.objects.all(),key=lambda podcast: podcast.sort_latest_episode(),reverse=True)
                #order by model custom function (sort_latest_episode)
        else:
            context['podcast'] = Podcast.objects.all()

        context['today'] = timezone.now().date  
        return context

class CategoryView(generic.DetailView):
    template_name='npr/category.html'
    model = Category
    context_object_name = 'selected_category'

    def get_context_data(self,**kwargs):
        context = super(CategoryView,self).get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        return context

class PodcastView(generic.DetailView):
    template_name='npr/podcast.html'
    model = Podcast
    context_object_name='podcast'

    def get_context_data(self,**kwargs):
        context = super(PodcastView,self).get_context_data(**kwargs)
        context['category'] = Category.objects.all()#pass in category list

        slug = self.kwargs.get('slug')
        # related podcast exlude showing podcast: get itself instance first, get its category via fk, then get podcasts under 
        #that category via fk, excluding slug field 
        context['related_podcast'] = Podcast.objects.get(slug=slug).category.podcast_set.all().exclude(slug=slug)

        n = self.kwargs.get('page') #catch thrown in page

        episodes = self.object.episode_set.all().order_by('-time')#order episodes by date

        paginator = Paginator(episodes,8)#each page 8 eps

        if n and n >=3:
            context['page_range'] = paginator.page_range[n-3:n+2]
        else:
            context['page_range'] = paginator.page_range[0:5]

        try:
            context['page_n'] = paginator.page(n)
        except PageNotAnInteger:
            context['page_n'] = paginator.page(1) #page 1 by default
        except EmptyPage:
            context['page_n'] = paginator.page(paginator.num_pages) #to last page 

        return context



def update_episode(request,p_id,slug):

    selected_pod = Podcast.objects.get(p_id=p_id) 

    e = UpdateEpisode(selected_pod.link,p_id) 

    E=e.render_episode() #get latest episodes ~24 or so

    existing_ep_list = selected_pod.episode_set.all() #get existing episodes

    def check_ep_exist(ep):

        ep_check = existing_ep_list.filter(slug=ep['slug']) #check if the query exist ep with same slug

        if ep_check.exists():
            return 
        else: #if not exist,create an episode
            new_ep = Episode(title=ep['title'],p_id=p_id,time = ep['time'],teaser = ep['teaser'],img_link=ep['img_link'],transcript_link=ep['transcript_link'],media_link=ep['media_link'],slug = ep['slug'])
            new_ep.save()
            return 

    for i in E:
        check_ep_exist(i)

    #redirect to podcast page
    return redirect(reverse('npr:podcast',args=(slug,)))

def search(request):
    try:
        #receive post request: search content
        search_content = request.POST.get('search_content')

        #podcast query with title containing search content
        result_podcast = Podcast.objects.filter(title__icontains=search_content)

        #episodes query with title or teaser containing search content
        result_episode = Episode.objects.filter( Q(title__icontains=search_content)|Q(teaser__icontains=search_content) )


    except ValueError:#catch search content value error
        raise Http404("No result found")

    else:
        context = {
        'category':Category.objects.all(),
        'search_content':search_content,
        'result_podcast':result_podcast,
        'result_episode':result_episode,
        }

    #render results in search.html 
        return render(request,"npr/search.html", context)




from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Page
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.utils.text import slugify
from django.contrib.auth.decorators import user_passes_test
from user.models import UserProgress
from django.views.decorators.http import require_POST
from django.contrib import messages

def get_seo_context(page_title, description, keywords):
    return {
        'page_title': f"{page_title} | MEO-BlogAI",
        'meta_description': description[:160],  # Max 160 karakter
        'meta_keywords': keywords,
        'og_title': page_title,
        'og_description': description[:200],  # Open Graph için biraz daha uzun
    }

def tr_slugify(text):
    tr_chars = {
        'ı': 'i', 'ğ': 'g', 'ü': 'u', 'ş': 's', 'ö': 'o', 'ç': 'c',
        'İ': 'i', 'Ğ': 'g', 'Ü': 'u', 'Ş': 's', 'Ö': 'o', 'Ç': 'c'
    }
    for char in tr_chars:
        text = text.replace(char, tr_chars[char])
    return slugify(text)

# Ana sayfa
def index(request):
    try:
        # Son güncellenen 3 içeriği al ve kategori kontrolü yap
        latest_contents = Page.objects.filter(
            category__in=['python', 'javascript', 'java', 'csharp', 'nlp', 'machinelearning']
        ).order_by('-last_update')[:3]

        # Statik görsel eşleştirmeleri
        content_images = {
            'python': 'img/python.jpeg',
            'javascript': 'img/javascript.jpeg',
            'java': 'img/java.jpeg',
            'csharp': 'img/csharp.jpeg',
            'nlp': 'img/nlp.jpeg',
            'machinelearning': 'img/makine.jpeg'
        }

        # Her içeriğe görsel ata
        for content in latest_contents:
            if content.category:  # Kategori boş değilse
                content.image_url = content_images.get(content.category.lower(), 'img/default-slide.jpg')
            else:
                content.image_url = 'img/default-slide.jpg'

        seo_context = get_seo_context(
            "Programlama ve Yapay Zeka Eğitimleri",
            "Ücretsiz programlama dersleri, yazılım eğitimleri ve yapay zeka içerikleri. Python, JavaScript, Java ve daha fazlası için MEO-BlogAI.",
            "programlama, yazılım, python, javascript, java, yapay zeka, eğitim"
        )

        context = {
            "latest_contents": latest_contents,
            "pages": Page.objects.all(),
            **seo_context
        }
        return render(request, 'pages/index.html', context)
    except Exception as e:
        print(f"Index error: {e}")  # Debug için
        return render(request, 'pages/index.html', {"error": str(e)})

# Hakkında sayfası
def about(request):
    return render(request, 'pages/about.html')

def show_language_page(request, language):
    if not request.user.is_authenticated:
        return redirect('login')
        
    # Sayfaları ID'ye göre sırala (en düşük ID'li sayfa ilk olacak)
    pages = Page.objects.filter(category=language.lower()).order_by('id')
    
    # Her sayfa için slug oluştur
    for page in pages:
        page.slug = tr_slugify(page.title)
    
    if pages.exists():
        first_page = pages.first()  # En düşük ID'li sayfayı al
    else:
        first_page = None

    seo_context = get_seo_context(
        f"{language.title()} Programlama Dersleri",
        f"{language.title()} programlama dili eğitimleri, örnekler ve projeler. Adım adım {language} öğrenin.",
        f"{language}, programlama, {language} dersleri, {language} eğitimi, yazılım"
    )

    context = {
        "pages": pages,
        "first_page": first_page,  # İlk sayfayı context'e ekle
        "language": language.title(),
        **seo_context
    }
    return render(request, 'pages/generic_language.html', context)

def mark_as_complete(request, page_id):
    page = get_object_or_404(Page, id=page_id)
    progress, created = UserProgress.objects.get_or_create(
        user=request.user,
        page=page
    )
    progress.completed = True
    progress.save()
    messages.success(request, "İlerlemeniz kaydedildi!")
    return redirect('language_detail', language=page.category, slug=page.slug)

def get_language_detail(request, language, slug):
    try:
        page = None
        page_id = request.GET.get('id')
        
        if page_id:
            page = Page.objects.get(id=page_id)
        else:
            page = Page.objects.get(
                category=language.lower(),
                title__iexact=slug.replace('-', ' ')
            )
        
        if not page:
            return HttpResponse(
                '<div class="alert alert-danger">'
                '<i class="fas fa-exclamation-circle me-2"></i>'
                'İçerik bulunamadı'
                '</div>'
            )
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return render(request, 'pages/detail.html', {
                "page": page,
                "is_admin": request.user.is_superuser
            })
            
        return render(request, 'pages/generic_language.html', {
            "page": page,
            "pages": Page.objects.filter(category=language.lower()),
            "language": language.title(),
            "is_admin": request.user.is_superuser
        })
        
    except Exception as e:
        print(f"Hata: {e}")
        return HttpResponse(
            '<div class="alert alert-danger">'
            '<i class="fas fa-exclamation-circle me-2"></i>'
            'Bir hata oluştu'
            '</div>'
        )

# Her dil için view fonksiyonları
def python(request):
    return show_language_page(request, "python")

def python_detail(request, slug):
    return get_language_detail(request, "python", slug)

def csharp(request):
    return show_language_page(request, "csharp")

def csharp_detail(request, slug):
    return get_language_detail(request, "csharp", slug)

def javascript(request):
    return show_language_page(request, "javascript")

def javascript_detail(request, slug):
    return get_language_detail(request, "javascript", slug)

def java(request):
    return show_language_page(request, "java")

def java_detail(request, slug):
    return get_language_detail(request, "java", slug)

# NLP sayfası
def nlp(request, title=None):
    if title:
        page = get_object_or_404(Page, title=slugify(title), category="nlp")
    else:
        page = Page.objects.filter(category="nlp")
    context = {
        "pages": page
    }
    return render(request, 'pages/nlp.html', context)

# Makine Öğrenmesi sayfası
def machinelearning(request, title=None):
    if title:
        page = get_object_or_404(Page, title=slugify(title), category="machinelearning")
    else:
        page = Page.objects.filter(category="machinelearning")
    context = {
        "pages": page
    }
    return render(request, 'pages/machinelearning.html', context)

def search(request):
    query = request.GET.get('q', '')
    if query:
        results = Page.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(category__icontains=query)
        ).distinct()
    else:
        results = []
    
    context = {
        'query': query,
        'results': results,
        'count': len(results)
    }
    return render(request, 'pages/search.html', context)

def is_admin(user):
    return user.is_superuser

@require_POST
@user_passes_test(is_admin)
def delete_page(request, page_id):
    try:
        page = get_object_or_404(Page, id=page_id)
        category = page.category
        page.delete()
        return JsonResponse({
            'status': 'success',
            'message': 'Sayfa başarıyla silindi',
            'redirect_url': f'/courses/{category}/'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

@require_POST
@user_passes_test(is_admin)
def save_page(request, page_id):
    try:
        page = get_object_or_404(Page, id=page_id)
        page.title = request.POST.get('title')
        page.content = request.POST.get('content')
        page.category = request.POST.get('category')
        page.save()
        return JsonResponse({
            'status': 'success',
            'message': 'İçerik başarıyla güncellendi'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error', 
            'message': str(e)
        }, status=500)

@user_passes_test(is_admin)
def edit_page(request, page_id):
    try:
        page = get_object_or_404(Page, id=page_id)
        if request.method == "GET":
            context = {
                'page': page,
                'categories': ['python', 'javascript', 'java', 'csharp', 'nlp', 'machinelearning']
            }
            return render(request, 'pages/edit_page.html', context)
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
from django.shortcuts import render, get_object_or_404
from .models import Page
from django.http import HttpResponse
from django.utils.text import slugify

def get_seo_context(page_title, description, keywords):
    return {
        'page_title': f"{page_title} | MEO-BlogAI",
        'meta_description': description[:160],  # Max 160 karakter
        'meta_keywords': keywords,
        'og_title': page_title,
        'og_description': description[:200],  # Open Graph için biraz daha uzun
    }

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
    pages = Page.objects.filter(category=language.lower()).order_by('id')
    # Her sayfa için slug oluştur
    for page in pages:
        page.slug = slugify(page.title)
    
    seo_context = get_seo_context(
        f"{language.title()} Programlama Dersleri",
        f"{language.title()} programlama dili eğitimleri, örnekler ve projeler. Adım adım {language} öğrenin.",
        f"{language}, programlama, {language} dersleri, {language} eğitimi, yazılım"
    )

    context = {
        "pages": pages,
        "language": language.title(),
        **seo_context
    }
    return render(request, 'pages/generic_language.html', context)

def get_language_detail(request, language, slug):
    try:
        # Tüm sayfaları al ve title'ı slug ile eşleşeni bul
        pages = Page.objects.filter(category=language.lower())
        page = next((p for p in pages if slugify(p.title) == slug), None)
        
        if not page:
            raise Page.DoesNotExist
            
        return render(request, 'pages/detail.html', {"page": page})
    except Page.DoesNotExist:
        print(f"Page not found: {language}/{slug}") # Debug için
        return HttpResponse(
            '<div class="alert alert-warning">İçerik bulunamadı</div>',
            status=404
        )
    except Exception as e:
        print(f"Error loading content: {e}") # Debug için
        return HttpResponse(
            f'<div class="alert alert-danger">Hata: {str(e)}</div>',
            status=500
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
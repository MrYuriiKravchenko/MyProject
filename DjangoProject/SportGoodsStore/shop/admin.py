from django.contrib import admin
from .models import Category, Product, Comment, Rating


class CommentAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'text', 'created']
    list_filter = ['created', 'user']
    search_fields = ['text', 'user__name', 'product__name']


class RatingAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'score']
    list_filter = ['score', 'user']
    search_fields = ['user__username', 'product__name']


class CommentInLine(admin.TabularInline):
    model = Comment
    extra = 0


class RatingInLine(admin.TabularInline):
    model = Rating
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price',
                    'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [CommentInLine, RatingInLine]


admin.site.register(Comment, CommentAdmin)
admin.site.register(Rating, RatingAdmin)

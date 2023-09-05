from django.contrib.auth.models import AbstractUser
from django.db import models

# Все новые классы регистрируй в админке

class User(AbstractUser):
    pass

class Post(models.Model):
    content = models.TextField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='post_likes', blank=True)

    def number_of_likes(self):
        return self.likes.count()

    # Отображение поста в админке
    def __str__(self):
        return f'Post{self.id} by {self.user} on {self.date.strftime("%d %b %Y %H:%M:%S")}'


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_who_is_following')
    user_follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_who_is_being_followed')

    def __str__(self):
        return f'{self.user} follows {self.user_follower}'

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name='user_likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default=None, related_name='post_likes')

    class Meta:
        unique_together = ('post', 'user')

    def __str__(self):
        return f"{self.user} likes {self.post}"



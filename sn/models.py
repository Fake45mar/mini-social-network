from django.db import models
# Create your models here.


class User(models.Model):
    class Meta:
        db_table = "user"
    user_name = models.CharField(max_length=50)
    user_mail = models.CharField(max_length=35)
    user_password = models.CharField(max_length=100)
    user_company = models.CharField(max_length=30)
    user_hunter_io = models.CharField(max_length=1000)
    user_clearbit_com = models.CharField(max_length=1000)
    user_online = models.BooleanField()


class Post(models.Model):
    class Meta:
        db_table = "post"
    post_title = models.CharField(max_length=200)
    post_text = models.TextField()
    post_date = models.DateTimeField()
    post_likes = models.IntegerField()
    post_user = models.ForeignKey(User, on_delete=models.CASCADE)


class LikedPost(models.Model):
    class Meta:
        db_table = "liked_post"
    liked_post_user = models.ForeignKey(User, on_delete=models.CASCADE)
    liked_post_post = models.ForeignKey(Post, on_delete=models.CASCADE)


class DisLikedPost(models.Model):
    class Meta:
        db_table = "disliked_post"
    disliked_post_user = models.ForeignKey(User, on_delete=models.CASCADE)
    disliked_post_post = models.ForeignKey(Post, on_delete=models.CASCADE)


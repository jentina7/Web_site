from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CASCADE


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        abstract = True


class UserProfile(AbstractUser):
    bio = models.CharField(max_length=200)
    image = models.ImageField(upload_to="user_images/")
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Follow(BaseModel):
    follower =models.ForeignKey(UserProfile, related_name="follower", on_delete=models.CASCADE)
    following = models.ForeignKey(UserProfile, related_name="following", on_delete=models.CASCADE)


class Post(BaseModel):
    user = models.ForeignKey(UserProfile, related_name="post_user", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="post_images/")
    video = models.FileField(upload_to="post_video/", blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    hashtag = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}-{self.image}"


class PostLike(BaseModel):
    user = models.ForeignKey(UserProfile, related_name="post_like_user", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="post_like", on_delete=models.CASCADE)
    like = models.BooleanField(default=False)

    class Meta:
        unique_together = ("user", "post")

    def __str__(self):
        return f"{self.user.username} likes {self.post} - {self.like}"


class Comment(BaseModel):
    post = models.ForeignKey(Post, related_name="post_comment", on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, related_name="comment_user", on_delete=models.CASCADE)
    text = models.TextField()
    parent = models.ForeignKey("self", related_name="replies", null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}, {self.post}"


class CommentLike(BaseModel):
    user = models.ForeignKey(UserProfile, related_name="comment_like_user", on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, related_name="comment_like", on_delete=models.CASCADE)
    like = models.BooleanField(default=False)

    class Meta:
        unique_together = ("user", "comment")

    def __str__(self):
        return f"{self.user.username} likes {self.comment.username} - {self.like}"


class Story(BaseModel):
    user = models.ForeignKey(UserProfile, related_name="story_user", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="story_images/")
    video = models.FileField(upload_to="story_video/", blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.image}, {self.video}"


class Save(models.Model):
    user = models.ForeignKey(UserProfile, related_name="save_user", on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class SaveItem(BaseModel):
    post = models.ForeignKey(Post, related_name="save_item_post", on_delete=models.CASCADE)
    save = models.ForeignKey(Save, on_delete=models.CASCADE)


class Chat(BaseModel):
    person = models.ManyToManyField(UserProfile)


class Massage(BaseModel):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="massage_images/", null=True, blank=True)
    video = models.FileField(upload_to="videos/", null=True, blank=True)


from django.db import models
from accounts.models import MyUser


# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=2000)
    FSK_CHOICES = [
        (0, 'FSK 0'),
        (6, 'FSK 6'),
        (12, 'FSK 12'),
        (16, 'FSK 16'),
        (18, 'FSK 18'),
    ]
    fsk = models.IntegerField(choices=FSK_CHOICES, default=0)
    GENRE_CHOICES = [
        ('C', 'Comedy'),
        ('A', 'Action'),
        ('R','Romance'),
        ('D', 'Drama'),
        ('H', 'Horror'),

    ]
    genre = models.CharField(choices=GENRE_CHOICES, max_length=2)
    year = models.IntegerField()
    director = models.TextField(max_length=100)
    time = models.IntegerField()
    actors = models.TextField(max_length=2000)
    price = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    details_pdf = models.FileField(upload_to='movie_pdfs/', null=True, blank=True)

    def __str__(self):
        return self.title
    def __repr__(self):
        return self.title + '/' + self.genre + '/' + self.fsk + '/' + self.year + '/' + self.time + '/' + self.director

class Rating(models.Model):
    STARS_CHOICES = [
        (1, '1 Stern'),
        (2, '2 Sterne'),
        (3, '3 Sterne'),
        (4, '4 Sterne'),
        (5, '5 Sterne'),
    ]
    text = models.TextField(max_length=500)
    stars = models.IntegerField(choices=STARS_CHOICES, default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'
        # Ein Benutzer kann einen Movie nur einmal bewerten
        unique_together = ('user', 'movie')

    def get_text_prefix(self):
        if len(self.text) > 50:
            return self.text[:50] + '...'
        else:
            return self.text

    def helpful_count(self):
        return self.ratingfeedback_set.filter(vote=1).count()

    def not_helpful_count(self):
        return self.ratingfeedback_set.filter(vote=0).count()

    def report_count(self):
        return self.ratingreport_set.count()

    def __str__(self):
        return self.get_text_prefix() + ' (' + self.user.username + ', ' + str(self.stars) + ' Sterne)'

    def __repr__(self):
        return self.get_text_prefix() + ' (' + self.user.username + ' / ' + str(self.timestamp) + ')'


class RatingFeedback(models.Model):
    UPVOTE = 1
    DOWNVOTE = 0

    VOTE_CHOICES = [
        (UPVOTE, 'Upvote'),
        (DOWNVOTE, 'Downvote'),
    ]

    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE)
    vote = models.IntegerField(choices=VOTE_CHOICES)

    class Meta:
        verbose_name = 'Rating Feedback'
        verbose_name_plural = 'Rating Feedbacks'
        # Ein Benutzer kann eine Bewertung nur einmal up oder down voten
        unique_together = ('user', 'rating')

class RatingReport(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE)
    reason = models.TextField(max_length=300, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Rating Report'
        verbose_name_plural = 'Rating Reports'
        # Ein Benutzer kann eine Bewertung nur einmal melden
        unique_together = ('user', 'rating')

    def __str__(self):
        return f'Meldung von {self.user.username} zu Rating #{self.rating.id}'
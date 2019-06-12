from django.db import models
from django.contrib.auth.models import User
# Create your models here.
# A model is just a class

class Topic(models.Model):
    """A topic the user is learning about"""
    #use CharField when you want to store a small
    #amount of text, such as a name, a title, or a city.
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        """Return a string representation of the model."""
        return self.text
    
class Entry(models.Model):
    """Something specific learned about a topic"""
    #Each entry needs to be associated with a particular topic.
    #This relationship is called a many-to-one relationship, 
    #meaning many entries can be associated with one topic.
    topic = models.ForeignKey('Topic', on_delete = models.CASCADE)
    #CASCADE: When the referenced object is deleted, 
    #also delete the objects that have references to it
    #The first attribute, topic, is a ForeignKey instance
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        """Meta holds extra information
        for managing a model; here it allows us to set a special attribute
        telling Django to use Entries when it needs 
        to refer to more than one entry (Without this, Django would refer
        to multiple entries as Entrys.)"""
        verbose_name_plural = 'entries'
        
    def __str__(self):
        """Return a string representation of the model."""
        #show just the first 50 characters of text
        if len(self.text)<50:
            return self.text[:50] 
        else:
            return self.text[:50] + "..."
        
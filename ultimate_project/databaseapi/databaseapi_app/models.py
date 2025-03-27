from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from utils.crypto import encrypt_2fa_secret, decrypt_2fa_secret


class PlayerManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username field must be set")

        email = self.normalize_email(email) if email else None
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)  # Hash the password before saving
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        return self.create_user(username, email, password, **extra_fields)


#  ================= MODELS MANAGED BY THIS MICROSERVICE (user) =================
class Player(AbstractBaseUser, PermissionsMixin):
    id          = models.AutoField(primary_key=True)
    username    = models.CharField(max_length=100, unique=True, blank=True)
    email       = models.EmailField(max_length=100, unique=True, blank=True, null=True)
    first_name  = models.CharField(max_length=100, blank=True)
    last_name   = models.CharField(max_length=100, blank=True)
    is_active   = models.BooleanField(default=True)
    is_staff    = models.BooleanField(default=False)  # needed for admin access
    # 2FA fields
    two_fa_enabled = models.BooleanField(default=False)  # 2FA toggle
    _two_fa_secret = models.CharField(max_length=32, blank=True, null=True)

    #friend list

    # Encrypt and decrypt 2FA secrets
    @property
    def two_fa_secret(self):
        return decrypt_2fa_secret(self._two_fa_secret) if self._two_fa_secret else None

    @two_fa_secret.setter
    def two_fa_secret(self, value):
        self._two_fa_secret = encrypt_2fa_secret(value) if value else None

    # Tells Django to use "email" as the primary field for authentication
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects = PlayerManager()  # Custom manager

    class Meta:
        db_table = "player"  # Explicitly set the schema and table name

    def __str__(self):
        return (f"Player: {self.first_name} {self.last_name} ({self.username}) | " \
            f"Email: {self.email if self.email else 'No email'} | " \
            f"Active: {'Yes' if self.is_active else 'No'} | " \
            f"Staff: {'Yes' if self.is_staff else 'No'} | " \
            f"2FA Enabled: {'Yes' if self.two_fa_enabled else 'No'}")
        
    # need toc reate a friend requets entry


class FriendList(models.Model):
    #one user for one friend list
    user = models.OneToOneField(Player, on_delete=models.CASCADE, related_name="user")
    friends = models.ManyToManyField(Player, blank=True, related_name="friends")
    
    def __str__(self):
        return self.user.username
    
    def add_friend(self, account):
        """
        Add a new friend
        """
        if not account in self.friends.all():
            self.friends.add(account)
            self.save()
    
    def remove_friend(self, account):
        """
        Remove friend
        """
        if account in self.friends.all():
            self.friends.remove(account)
            self.save()
    
    def unfriend(self, removee):
        """
        initiate the action of unfriending someone
        """
        remover_friends_list = self #person terminating the friendship
        # Remove friend from remover friend list
        remover_friends_list.remove_friend(removee)
        #Remove the friend from removee friend list
        friends_list_removee = FriendList.objects.get(user=removee)
        friends_list_removee.remove_friend(self.user)
        
    def is_mutual_friend(self, friend):
        """
        Check if it's a fiend
        """
        if friend in self.friends.all():
            return (True)
        return (False)
            
class FriendRequest(models.Model):
    #because a user can send an ulimited number of friend request
    sender = models.ForeignKey(to=Player, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(to=Player, on_delete=models.CASCADE, related_name="receiver")
    
    # friend request inactive if accepted/declined
    # by default when created is active
    is_active = models.BooleanField(blank=True, null=False, default=True)       
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
    # Format: Sender -> Receiver (Timestamp, Active Status)
        return (f"FriendRequest: {self.sender.username} -> {self.receiver.username} | " \
            f"Sent at: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')} | " \
            f"Status: {'Active' if self.is_active else 'Inactive'}")

    def accept(self):
        """
        Accept a friend request
        Update both sender and receiver friend list
        """
        receiver_friend_list: FriendList = FriendList.objects.get(user=self.receiver)
        if receiver_friend_list:
            receiver_friend_list.add_friend(self.sender)
            sender_friend_list: FriendList = FriendList.objects.get(user=self.sender)
            if sender_friend_list:
                sender_friend_list.add_friend(self.receiver)
                self.is_active = False
                self.save()
    
    def decline(self):
        """
        Decline a friend request by settign is_active to false
        """
        self.is_active = False
        self.save()
    
    def cancel(self):
        """
        Cancel a friend request from sender perspective
        different than decline based on notification
        """
        self.is_active = False
        self.save()
        

class Tournament(models.Model):
    id = models.AutoField(primary_key=True)

    class Meta:
        db_table = "tournament"

    def __str__(self):
        return f"Tournament {self.id}"


class Match(models.Model):
    id = models.AutoField(primary_key=True)

    player1 = models.ForeignKey(
        to=Player,  # Explicit reference to Player model
        on_delete=models.CASCADE,  # If a player is deleted, the match is also deleted
        related_name="player1",
    )
    player2 = models.ForeignKey(
        to=Player,
        on_delete=models.CASCADE,
        related_name="player2",
    )
    winner = models.ForeignKey(
        to=Player,
        on_delete=models.CASCADE,
        related_name="winner",
    )

    tournament = models.ForeignKey(
        to=Tournament,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "match"

    def __str__(self):
        return f"Match {self.id}"

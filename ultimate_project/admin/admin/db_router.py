class MultiDBRouter:
    """
    A router to control all database operations on models for different
    databases.
    """

    def db_for_read(self, model, **hints):
        """
        Attempts to read models go to the database associated with the model.
        """
        if model._meta.app_label == 'users_app':
            return 'users'
        elif model._meta.app_label == 'matches_app':
            return 'matches'
        elif model._meta.app_label == 'tournaments_app':
            return 'tournaments'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write models go to the database associated with the model.
        """
        if model._meta.app_label == 'users_app':
            return 'users'
        elif model._meta.app_label == 'matches_app':
            return 'matches'
        elif model._meta.app_label == 'tournaments_app':
            return 'tournaments'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the users, matches, or tournaments apps is
        involved.
        """
        if obj1._meta.app_label in ['users_app', 'matches_app', 'tournaments_app'] or obj2._meta.app_label in ['users_app', 'matches_app', 'tournaments_app']:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the users, matches, and tournaments apps only appear in the
        related databases.
        """
        if app_label == 'users_app':
            return db == 'users'
        elif app_label == 'matches_app':
            return db == 'matches'
        elif app_label == 'tournaments_app':
            return db == 'tournaments'
        return None

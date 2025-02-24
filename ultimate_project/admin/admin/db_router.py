# admin/db_router.py
class AdminRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'user_app':
            return 'user_db'
        elif model._meta.app_label == 'match_app':
            return 'match_db'
        elif model._meta.app_label == 'tournament_app':
            return 'tournament_db'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'user_app':
            return 'user_db'
        elif model._meta.app_label == 'match_app':
            return 'match_db'
        elif model._meta.app_label == 'tournament_app':
            return 'tournament_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return None

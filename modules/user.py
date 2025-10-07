from .supabase_client import get_supabase_client

class User:
    @staticmethod
    def sign_up(email, password, username):
        """Signs up a new user using Supabase Auth."""
        supabase = get_supabase_client()
        try:
            # Supabase handles email verification, so users are signed up but may need to confirm.
            res = supabase.auth.sign_up({
                "email": email,
                "password": password,
                "options": {
                    "data": {
                        "username": username,
                        "subscription_plan": "Starter",
                        "completed_tasks": []
                    }
                }
            })
            # After signing up, create a corresponding user profile in the 'profiles' table
            if res.user:
                supabase.table('profiles').insert({
                    'id': res.user.id,
                    'username': username,
                    'email': email
                }).execute()
            return res, None
        except Exception as e:
            return None, e

    @staticmethod
    def sign_in(email, password):
        """Signs in a user using Supabase Auth."""
        supabase = get_supabase_client()
        try:
            res = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            return res, None
        except Exception as e:
            return None, e

    @staticmethod
    def sign_out():
        """Signs out the current user."""
        supabase = get_supabase_client()
        try:
            res = supabase.auth.sign_out()
            return res, None
        except Exception as e:
            return None, e

    @staticmethod
    def get_profile(user_id):
        """Gets a user's profile from the 'profiles' table."""
        supabase = get_supabase_client()
        try:
            res = supabase.table('profiles').select("*").eq('id', user_id).single().execute()
            return res.data, None
        except Exception as e:
            return None, e

    @staticmethod
    def add_completed_task(user_id, task_text):
        """Adds a completed task to a user's profile."""
        supabase = get_supabase_client()
        try:
            # First, get the current list of completed tasks
            profile, error = User.get_profile(user_id)
            if error:
                raise error

            current_tasks = profile.get('completed_tasks', [])
            if task_text not in current_tasks:
                current_tasks.append(task_text)

            # Now, update the profile with the new list
            res = supabase.table('profiles').update({'completed_tasks': current_tasks}).eq('id', user_id).execute()
            return res, None
        except Exception as e:
            return None, e
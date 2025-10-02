from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Etudiant, Enseignant


class Command(BaseCommand):
    help = 'Réinitialiser les mots de passe de tous les utilisateurs'

    def add_arguments(self, parser):
        parser.add_argument(
            '--password',
            type=str,
            default='password123',
            help='Mot de passe à définir (par défaut: password123)'
        )

    def handle(self, *args, **options):
        password = options['password']
        
        self.stdout.write('Réinitialisation des mots de passe...')
        
        # Réinitialiser les mots de passe des étudiants
        etudiants = User.objects.filter(etudiant__isnull=False)
        for user in etudiants:
            user.set_password(password)
            user.save()
            self.stdout.write(f'✓ Étudiant: {user.username}')
        
        # Réinitialiser les mots de passe des enseignants
        enseignants = User.objects.filter(enseignant__isnull=False)
        for user in enseignants:
            user.set_password(password)
            user.save()
            self.stdout.write(f'✓ Enseignant: {user.username}')
        
        # Réinitialiser le mot de passe admin si nécessaire
        try:
            admin = User.objects.get(username='admin')
            admin.set_password('admin123')
            admin.save()
            self.stdout.write(f'✓ Admin: admin')
        except User.DoesNotExist:
            pass
        
        self.stdout.write(
            self.style.SUCCESS(f'\nMots de passe réinitialisés avec succès!')
        )
        self.stdout.write('Comptes de connexion:')
        self.stdout.write('- Admin: admin / admin123')
        self.stdout.write(f'- Enseignants: martin.dupont / {password}')
        self.stdout.write(f'- Étudiants: et001 / {password}')
        self.stdout.write(f'\nTous les utilisateurs ont maintenant le mot de passe: {password}')

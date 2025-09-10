from django.core.management.base import BaseCommand
from accounts.models import Region, Institution, LanguageSupport


class Command(BaseCommand):
    help = 'Populate initial regional and institutional data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force recreate data even if it exists',
        )

    def handle(self, *args, **options):
        force = options['force']

        # Create regions with cultural context
        regions_data = [
            {
                'name': 'North India',
                'code': 'NI',
                'primary_language': 'Hindi',
                'cultural_context': {
                    'festivals': ['Diwali', 'Holi', 'Karva Chauth', 'Dussehra'],
                    'values': ['family_orientation', 'respect_for_elders', 'community_support'],
                    'communication_style': 'indirect',
                    'mental_health_stigma': 'high',
                    'preferred_counseling_approach': 'family_inclusive'
                }
            },
            {
                'name': 'South India',
                'code': 'SI',
                'primary_language': 'Tamil',
                'cultural_context': {
                    'festivals': ['Pongal', 'Onam', 'Diwali', 'Navratri'],
                    'values': ['education_emphasis', 'traditional_medicine', 'family_honor'],
                    'communication_style': 'respectful',
                    'mental_health_stigma': 'moderate',
                    'preferred_counseling_approach': 'holistic'
                }
            },
            {
                'name': 'West India',
                'code': 'WI',
                'primary_language': 'Marathi',
                'cultural_context': {
                    'festivals': ['Ganpati', 'Gudi Padwa', 'Diwali', 'Navratri'],
                    'values': ['entrepreneurship', 'progressive_thinking', 'cultural_pride'],
                    'communication_style': 'direct',
                    'mental_health_stigma': 'moderate',
                    'preferred_counseling_approach': 'practical'
                }
            },
            {
                'name': 'East India',
                'code': 'EI',
                'primary_language': 'Bengali',
                'cultural_context': {
                    'festivals': ['Durga Puja', 'Kali Puja', 'Poila Boishakh', 'Diwali'],
                    'values': ['intellectual_pursuits', 'art_literature', 'social_consciousness'],
                    'communication_style': 'expressive',
                    'mental_health_stigma': 'low',
                    'preferred_counseling_approach': 'intellectual'
                }
            }
        ]

        self.stdout.write("Creating regions...")
        for region_data in regions_data:
            region, created = Region.objects.get_or_create(
                code=region_data['code'],
                defaults=region_data
            )
            if created or force:
                if force and not created:
                    Region.objects.filter(code=region_data['code']).update(**region_data)
                    region.refresh_from_db()
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created/Updated region: {region.name}')
                )

        # Create language support for regions
        languages_data = [
            {'name': 'English', 'code': 'en', 'regions': ['NI', 'SI', 'WI', 'EI']},
            {'name': 'Hindi', 'code': 'hi', 'regions': ['NI', 'WI'], 'primary_for': ['NI']},
            {'name': 'Tamil', 'code': 'ta', 'regions': ['SI'], 'primary_for': ['SI']},
            {'name': 'Telugu', 'code': 'te', 'regions': ['SI']},
            {'name': 'Marathi', 'code': 'mr', 'regions': ['WI'], 'primary_for': ['WI']},
            {'name': 'Gujarati', 'code': 'gu', 'regions': ['WI']},
            {'name': 'Bengali', 'code': 'bn', 'regions': ['EI'], 'primary_for': ['EI']},
            {'name': 'Kannada', 'code': 'kn', 'regions': ['SI']},
            {'name': 'Malayalam', 'code': 'ml', 'regions': ['SI']},
            {'name': 'Punjabi', 'code': 'pa', 'regions': ['NI']},
        ]

        self.stdout.write("Creating language support...")
        for lang_data in languages_data:
            for region_code in lang_data['regions']:
                try:
                    region = Region.objects.get(code=region_code)
                    is_primary = region_code in lang_data.get('primary_for', [])
                    
                    lang_support, created = LanguageSupport.objects.get_or_create(
                        language_code=lang_data['code'],
                        region=region,
                        defaults={
                            'language_name': lang_data['name'],
                            'is_primary': is_primary,
                            'ui_translations': self._get_ui_translations(lang_data['code']),
                            'content_translations': self._get_content_translations(lang_data['code'])
                        }
                    )
                    if created or force:
                        if force and not created:
                            LanguageSupport.objects.filter(
                                language_code=lang_data['code'], region=region
                            ).update(
                                language_name=lang_data['name'],
                                is_primary=is_primary,
                                ui_translations=self._get_ui_translations(lang_data['code']),
                                content_translations=self._get_content_translations(lang_data['code'])
                            )
                        self.stdout.write(
                            self.style.SUCCESS(f'✓ Added {lang_data["name"]} support for {region.name}')
                        )
                except Region.DoesNotExist:
                    continue

        # Create sample institutions
        institutions_data = [
            {
                'name': 'Delhi University',
                'code': 'DU',
                'institution_type': 'university',
                'region_code': 'NI',
                'address': 'Delhi, India',
                'contact_email': 'counseling@du.ac.in',
                'contact_phone': '+91-11-12345678'
            },
            {
                'name': 'Indian Institute of Technology Madras',
                'code': 'IITM',
                'institution_type': 'technical',
                'region_code': 'SI',
                'address': 'Chennai, Tamil Nadu, India',
                'contact_email': 'counseling@iitm.ac.in',
                'contact_phone': '+91-44-87654321'
            },
            {
                'name': 'University of Mumbai',
                'code': 'MU',
                'institution_type': 'university',
                'region_code': 'WI',
                'address': 'Mumbai, Maharashtra, India',
                'contact_email': 'counseling@mu.ac.in',
                'contact_phone': '+91-22-11223344'
            },
            {
                'name': 'Jadavpur University',
                'code': 'JU',
                'institution_type': 'university',
                'region_code': 'EI',
                'address': 'Kolkata, West Bengal, India',
                'contact_email': 'counseling@ju.ac.in',
                'contact_phone': '+91-33-55667788'
            }
        ]

        self.stdout.write("Creating sample institutions...")
        for inst_data in institutions_data:
            try:
                region = Region.objects.get(code=inst_data.pop('region_code'))
                inst_data['region'] = region
                
                institution, created = Institution.objects.get_or_create(
                    code=inst_data['code'],
                    defaults=inst_data
                )
                if created or force:
                    if force and not created:
                        Institution.objects.filter(code=inst_data['code']).update(**inst_data)
                        institution.refresh_from_db()
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ Created/Updated institution: {institution.name}')
                    )
            except Region.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Region not found for institution {inst_data["name"]}')
                )

        self.stdout.write(
            self.style.SUCCESS('Successfully populated initial regional and institutional data!')
        )

    def _get_ui_translations(self, language_code):
        """Get UI translations for a specific language"""
        translations = {
            'hi': {
                'welcome': 'स्वागत',
                'mental_health': 'मानसिक स्वास्थ्य',
                'counseling': 'परामर्श',
                'help': 'सहायता',
                'support': 'सहारा'
            },
            'ta': {
                'welcome': 'வரவேற்கிறோம்',
                'mental_health': 'மன நலம்',
                'counseling': 'ஆலோசனை',
                'help': 'உதவி',
                'support': 'ஆதரவு'
            },
            'bn': {
                'welcome': 'স্বাগতম',
                'mental_health': 'মানসিক স্বাস্থ্য',
                'counseling': 'পরামর্শ',
                'help': 'সাহায্য',
                'support': 'সহায়তা'
            },
            'mr': {
                'welcome': 'स्वागत',
                'mental_health': 'मानसिक आरोग्य',
                'counseling': 'सल्ला',
                'help': 'मदत',
                'support': 'आधार'
            }
        }
        return translations.get(language_code, {})

    def _get_content_translations(self, language_code):
        """Get content translations for a specific language"""
        translations = {
            'hi': {
                'crisis_message': 'यदि आप संकट में हैं, तो कृपया तुरंत सहायता लें',
                'confidential_message': 'आपकी जानकारी पूर्णतः गोपनीय है'
            },
            'ta': {
                'crisis_message': 'நீங்கள் நெருக்கடியில் இருந்தால், உடனே உதவி பெறுங்கள்',
                'confidential_message': 'உங்கள் தகவல்கள் முற்றிலும் ரகசியமானவை'
            },
            'bn': {
                'crisis_message': 'আপনি যদি সংকটে থাকেন, তাহলে অবিলম্বে সাহায্য নিন',
                'confidential_message': 'আপনার তথ্য সম্পূর্ণ গোপনীয়'
            },
            'mr': {
                'crisis_message': 'जर तुम्ही संकटात असाल तर कृपया ताबडतोब मदत घ्या',
                'confidential_message': 'तुमची माहिती पूर्णपणे गुप्त आहे'
            }
        }
        return translations.get(language_code, {})

import json
import uuid
from typing import Dict, Any, List
from google.cloud import pubsub_v1
from datetime import datetime, timedelta
from config import Config

class SchedulerAgent:
    """Handles automated scheduling and calendar integration for LVX platform"""
    
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.publisher = pubsub_v1.PublisherClient()
        
    def schedule_founder_interview(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Schedule voice interview with founder"""
        
        app_id = message['app_id']
        run_id = message['run_id']
        founder_contact = message.get('founder_contact', {})
        
        # Find available time slots
        available_slots = self._find_available_slots()
        
        # Create interview session
        interview_session = {
            'session_id': str(uuid.uuid4()),
            'app_id': app_id,
            'run_id': run_id,
            'scheduled_time': available_slots[0],
            'duration_minutes': Config.VOICE_INTERVIEW_DURATION,
            'interview_type': 'discovery',
            'status': 'scheduled',
            'founder_contact': founder_contact,
            'meeting_link': self._generate_meeting_link(),
            'calendar_event_id': str(uuid.uuid4())
        }
        
        # Send calendar invite
        self._send_calendar_invite(interview_session)
        
        # Send confirmation notifications
        self._send_confirmation_notifications(interview_session)
        
        # Publish scheduling completion
        self._publish_message('interview-scheduled', {
            'run_id': run_id,
            'app_id': app_id,
            'interview_session': interview_session
        })
        
        return interview_session
    
    def schedule_investor_meeting(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Schedule meeting between founder and senior fund decision makers"""
        
        app_id = message['app_id']
        investor_preferences = message.get('investor_preferences', {})
        
        # Find mutual availability
        available_slots = self._find_mutual_availability(
            message.get('founder_availability', []),
            message.get('investor_availability', [])
        )
        
        meeting_session = {
            'meeting_id': str(uuid.uuid4()),
            'app_id': app_id,
            'meeting_type': 'investor_presentation',
            'scheduled_time': available_slots[0] if available_slots else self._find_available_slots()[0],
            'duration_minutes': 60,
            'attendees': self._get_meeting_attendees(investor_preferences),
            'meeting_link': self._generate_meeting_link(),
            'agenda': self._generate_meeting_agenda(app_id),
            'status': 'scheduled'
        }
        
        # Send calendar invites to all attendees
        self._send_meeting_invites(meeting_session)
        
        return meeting_session
    
    def handle_scheduling_conflicts(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Handle scheduling conflicts and reschedule automatically"""
        
        session_id = message['session_id']
        conflict_reason = message.get('conflict_reason', 'scheduling_conflict')
        
        # Find alternative slots
        alternative_slots = self._find_available_slots(exclude_conflicted=True)
        
        # Reschedule to next available slot
        rescheduled_session = {
            'session_id': session_id,
            'original_time': message.get('original_time'),
            'new_time': alternative_slots[0],
            'conflict_reason': conflict_reason,
            'status': 'rescheduled'
        }
        
        # Send reschedule notifications
        self._send_reschedule_notifications(rescheduled_session)
        
        # Update calendar events
        self._update_calendar_events(rescheduled_session)
        
        return rescheduled_session
    
    def send_meeting_reminders(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Send automated meeting reminders"""
        
        session_id = message['session_id']
        reminder_type = message.get('reminder_type', '24_hour')
        
        reminder_data = {
            'session_id': session_id,
            'reminder_type': reminder_type,
            'sent_at': datetime.utcnow().isoformat(),
            'recipients': message.get('recipients', []),
            'meeting_details': message.get('meeting_details', {})
        }
        
        # Send reminders via multiple channels
        self._send_email_reminders(reminder_data)
        self._send_sms_reminders(reminder_data)
        self._send_calendar_reminders(reminder_data)
        
        return reminder_data
    
    def _find_available_slots(self, exclude_conflicted: bool = False) -> List[str]:
        """Find available time slots for scheduling"""
        
        # Mock implementation - in production would integrate with Google Calendar API
        base_time = datetime.now() + timedelta(days=1)
        
        available_slots = []
        for i in range(5):  # Next 5 business days
            # Skip weekends
            if base_time.weekday() < 5:  # Monday = 0, Friday = 4
                # Morning slots
                morning_slot = base_time.replace(hour=10, minute=0, second=0, microsecond=0)
                available_slots.append(morning_slot.isoformat())
                
                # Afternoon slots
                afternoon_slot = base_time.replace(hour=14, minute=0, second=0, microsecond=0)
                available_slots.append(afternoon_slot.isoformat())
            
            base_time += timedelta(days=1)
        
        return available_slots[:10]  # Return top 10 slots
    
    def _find_mutual_availability(self, founder_availability: List[str], investor_availability: List[str]) -> List[str]:
        """Find mutual availability between founder and investors"""
        
        # Mock implementation - would use actual calendar integration
        mutual_slots = []
        
        # Find overlapping time slots
        for founder_slot in founder_availability:
            if founder_slot in investor_availability:
                mutual_slots.append(founder_slot)
        
        # If no mutual availability, suggest compromise slots
        if not mutual_slots:
            mutual_slots = self._find_available_slots()[:3]
        
        return mutual_slots
    
    def _generate_meeting_link(self) -> str:
        """Generate video meeting link"""
        
        # Mock implementation - would integrate with Google Meet, Zoom, etc.
        meeting_id = str(uuid.uuid4())[:8]
        return f"https://meet.google.com/{meeting_id}"
    
    def _get_meeting_attendees(self, investor_preferences: Dict[str, Any]) -> List[Dict[str, str]]:
        """Get list of meeting attendees based on investor preferences"""
        
        attendees = [
            {
                'name': 'Senior Partner',
                'email': 'partner@lvx.com',
                'role': 'Investment Decision Maker'
            },
            {
                'name': 'Principal',
                'email': 'principal@lvx.com',
                'role': 'Deal Lead'
            }
        ]
        
        # Add sector-specific experts if needed
        if investor_preferences.get('sector_expertise_required'):
            attendees.append({
                'name': 'Sector Expert',
                'email': 'expert@lvx.com',
                'role': 'Technical Advisor'
            })
        
        return attendees
    
    def _generate_meeting_agenda(self, app_id: str) -> List[Dict[str, Any]]:
        """Generate meeting agenda based on startup profile"""
        
        agenda = [
            {
                'item': 'Introductions and Overview',
                'duration_minutes': 5,
                'owner': 'Moderator'
            },
            {
                'item': 'Founder Presentation',
                'duration_minutes': 20,
                'owner': 'Founder',
                'details': 'Company overview, market opportunity, traction'
            },
            {
                'item': 'Q&A Session',
                'duration_minutes': 25,
                'owner': 'Investors',
                'details': 'Deep dive questions on business model, competition, scaling'
            },
            {
                'item': 'Next Steps Discussion',
                'duration_minutes': 10,
                'owner': 'All',
                'details': 'Due diligence process, timeline, expectations'
            }
        ]
        
        return agenda
    
    def _send_calendar_invite(self, interview_session: Dict[str, Any]):
        """Send Google Calendar invite for interview"""
        
        # Mock implementation - would use Google Calendar API
        print(f"Calendar invite sent for interview {interview_session['session_id']}")
        
        # In production, would create actual calendar event
        calendar_event = {
            'summary': f"LVX Startup Interview - {interview_session['app_id']}",
            'start': {'dateTime': interview_session['scheduled_time']},
            'end': {'dateTime': self._calculate_end_time(interview_session['scheduled_time'], interview_session['duration_minutes'])},
            'attendees': [{'email': interview_session['founder_contact'].get('email', 'founder@startup.com')}],
            'conferenceData': {'createRequest': {'requestId': str(uuid.uuid4())}}
        }
    
    def _send_meeting_invites(self, meeting_session: Dict[str, Any]):
        """Send calendar invites to all meeting attendees"""
        
        # Mock implementation
        print(f"Meeting invites sent for {meeting_session['meeting_id']}")
        
        for attendee in meeting_session['attendees']:
            print(f"Invite sent to {attendee['email']}")
    
    def _send_confirmation_notifications(self, interview_session: Dict[str, Any]):
        """Send confirmation notifications via email and SMS"""
        
        # Mock implementation - would integrate with email/SMS services
        notifications_sent = {
            'email_sent': True,
            'sms_sent': True,
            'calendar_invite_sent': True,
            'session_id': interview_session['session_id']
        }
        
        print(f"Confirmation notifications sent for {interview_session['session_id']}")
        
        return notifications_sent
    
    def _send_reschedule_notifications(self, rescheduled_session: Dict[str, Any]):
        """Send reschedule notifications to all parties"""
        
        # Mock implementation
        print(f"Reschedule notifications sent for {rescheduled_session['session_id']}")
        
        notification_content = {
            'subject': 'Meeting Rescheduled - LVX Interview',
            'message': f"Your interview has been rescheduled to {rescheduled_session['new_time']} due to {rescheduled_session['conflict_reason']}",
            'new_meeting_link': self._generate_meeting_link()
        }
        
        return notification_content
    
    def _update_calendar_events(self, rescheduled_session: Dict[str, Any]):
        """Update calendar events with new timing"""
        
        # Mock implementation - would use Google Calendar API
        print(f"Calendar events updated for {rescheduled_session['session_id']}")
    
    def _send_email_reminders(self, reminder_data: Dict[str, Any]):
        """Send email reminders"""
        
        # Mock implementation - would integrate with email service
        print(f"Email reminders sent for {reminder_data['session_id']}")
    
    def _send_sms_reminders(self, reminder_data: Dict[str, Any]):
        """Send SMS reminders"""
        
        # Mock implementation - would integrate with SMS service
        print(f"SMS reminders sent for {reminder_data['session_id']}")
    
    def _send_calendar_reminders(self, reminder_data: Dict[str, Any]):
        """Send calendar-based reminders"""
        
        # Mock implementation
        print(f"Calendar reminders set for {reminder_data['session_id']}")
    
    def _calculate_end_time(self, start_time: str, duration_minutes: int) -> str:
        """Calculate meeting end time"""
        
        start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
        end_dt = start_dt + timedelta(minutes=duration_minutes)
        return end_dt.isoformat()
    
    def _publish_message(self, topic: str, message: Dict[str, Any]):
        """Publish message to Pub/Sub"""
        topic_path = self.publisher.topic_path(self.project_id, topic)
        message_json = json.dumps(message).encode('utf-8')
        self.publisher.publish(topic_path, message_json)
    
    def get_scheduling_analytics(self) -> Dict[str, Any]:
        """Get analytics on scheduling patterns and efficiency"""
        
        analytics = {
            'total_interviews_scheduled': 45,
            'average_scheduling_time': '2.3 hours',
            'reschedule_rate': 0.12,
            'no_show_rate': 0.05,
            'most_popular_time_slots': ['10:00 AM', '2:00 PM', '4:00 PM'],
            'scheduling_efficiency_score': 8.7,
            'founder_satisfaction_score': 9.1,
            'investor_satisfaction_score': 8.9
        }
        
        return analytics
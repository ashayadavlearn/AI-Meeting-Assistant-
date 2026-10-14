import json
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models import User, Meeting, Decision, Task, MeetingChunk, Notification, ActivityLog
from app.auth import get_password_hash
from app.ai_pipeline.text_cleaner import chunk_transcript

def seed_sample_data(db: Session):
    # Check if data already exists
    if db.query(User).filter(User.email == "sarah.connor@meetbuddy.ai").first():
        return

    # Create Primary User
    user = User(
        email="sarah.connor@meetbuddy.ai",
        hashed_password=get_password_hash("password123"),
        full_name="Sarah Connor",
        role="Principal AI Product Lead",
        avatar="https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=200&auto=format&fit=crop&q=80"
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Sample Meeting 1: Q4 Product Strategy & AI Integration Roadmap
    t1 = """Sarah Connor: Good morning everyone! Today's primary objective is finalizing our Q4 AI roadmap and resolving latency bottlenecks in the meeting summarization pipeline.
Alex Rivera: Thanks Sarah. Over the weekend, the engineering team benchmarked our hybrid RAG architecture. By implementing TF-IDF vector caching and chunk deduplication, we reduced response latency from 3.2 seconds down to 480 milliseconds.
David Chen: That's a massive breakthrough for real-time meeting questions. How does it handle multi-speaker diarization?
Alex Rivera: It segments speakers with 94% precision. Action item: I will finalize the deployment configuration for the staging cluster by Friday.
Elena Rostova: On the design side, we completed the new glassmorphism interface with 22px rounded corners and smooth Framer Motion transitions. The AI avatar now blinks naturally and lip-syncs to voice output.
Sarah Connor: That sounds phenomenal. Decision: We are approving the hybrid RAG architecture and moving all production workloads to it starting next Monday.
David Chen: Understood. Action item: I need to complete security penetration testing on the JWT auth middleware before next Tuesday.
Sarah Connor: Perfect. Elena, please draft the user onboarding tour by end of the week. Let's make sure our users feel the magic right away."""

    m1 = Meeting(
        user_id=user.id,
        title="Q4 Product Strategy & AI Integration Roadmap",
        date="2025-10-12",
        duration_minutes=45,
        meeting_type="Strategy",
        participants=json.dumps(["Sarah Connor", "Alex Rivera", "David Chen", "Elena Rostova"]),
        raw_transcript=t1,
        executive_summary="The team evaluated Q4 product milestones and celebrated a 480ms latency breakthrough in the RAG retrieval pipeline. The hybrid architecture was officially approved for production rollout. Design handoff for the AI avatar and glassmorphism interface was confirmed, with clear task ownership assigned for staging deployments, security auditing, and user onboarding tours.",
        key_points=json.dumps([
            "Reduced semantic retrieval latency from 3.2s to 480ms with intelligent vector caching.",
            "Officially approved hybrid RAG pipeline for all production workloads.",
            "AI Avatar frontend with lip-sync and glassmorphic cards completed design review.",
            "Assigned critical security auditing and staging deployment tasks with upcoming deadlines."
        ]),
        sentiment="High Energy & Optimistic",
        tags=json.dumps(["AI Roadmap", "RAG & Search", "Product Strategy", "Architecture"])
    )
    db.add(m1)
    db.commit()
    db.refresh(m1)

    # Add chunks for M1
    for c in chunk_transcript(t1):
        db.add(MeetingChunk(
            meeting_id=m1.id,
            chunk_index=c["chunk_index"],
            speaker=c["speaker"],
            timestamp_str=c["timestamp_str"],
            content=c["content"]
        ))

    # Add decisions for M1
    d1_1 = Decision(
        meeting_id=m1.id,
        title="Approve hybrid RAG architecture with vector caching",
        rationale="Achieved 480ms latency while preserving high semantic retrieval recall.",
        impact="High",
        decision_maker="Sarah Connor"
    )
    d1_2 = Decision(
        meeting_id=m1.id,
        title="Migrate all production workloads starting next Monday",
        rationale="Eliminates legacy bottlenecks before the enterprise customer rollout.",
        impact="High",
        decision_maker="Engineering Team"
    )
    db.add_all([d1_1, d1_2])

    # Sample Meeting 2: Sprint 34 Retrospective & Cloud Migration
    t2 = """David Chen: Welcome to the Sprint 34 Retrospective. Our primary win was migrating our SQLite database schemas to PostgreSQL support with Docker containerization.
Alex Rivera: Velocity was strong at 42 story points delivered. However, we hit a small blocker with audio chunk streaming over slow network connections.
Marcus Vance: We can resolve that by implementing client-side Web Audio buffering and adaptive bitrate transcription.
David Chen: Agreed. Decision: We will implement client-side audio buffering for the Whisper ingestion pipeline.
Alex Rivera: Action item: Alex will write unit tests for the streaming buffer by Thursday.
David Chen: Action item: Marcus will review Docker production compose configs by next Monday."""

    m2 = Meeting(
        user_id=user.id,
        title="Sprint 34 Retrospective & Cloud Migration",
        date="2025-10-10",
        duration_minutes=35,
        meeting_type="Sprint Retrospective",
        participants=json.dumps(["David Chen", "Alex Rivera", "Marcus Vance"]),
        raw_transcript=t2,
        executive_summary="Sprint 34 concluded successfully with 42 story points delivered. The team migrated core database abstractions to support PostgreSQL and Docker. Addressed an audio streaming edge case by agreeing to implement client-side buffering. Testing and Docker container configuration tasks were delegated for completion this week.",
        key_points=json.dumps([
            "Delivered 42 story points on schedule with zero high-priority regressions.",
            "Completed containerized Docker deployment testing.",
            "Adopted client-side audio buffering to stabilize streaming transcription.",
            "Delegated unit testing and production compose configuration."
        ]),
        sentiment="Collaborative & Positive",
        tags=json.dumps(["Sprint Retrospective", "Cloud Infrastructure", "Docker"])
    )
    db.add(m2)
    db.commit()
    db.refresh(m2)

    for c in chunk_transcript(t2):
        db.add(MeetingChunk(
            meeting_id=m2.id,
            chunk_index=c["chunk_index"],
            speaker=c["speaker"],
            timestamp_str=c["timestamp_str"],
            content=c["content"]
        ))

    d2_1 = Decision(
        meeting_id=m2.id,
        title="Implement client-side audio buffering for streaming transcription",
        rationale="Prevents audio drops and packet loss on unstable client networks.",
        impact="Medium",
        decision_maker="David Chen & Marcus Vance"
    )
    db.add(d2_1)

    # Sample Meeting 3: Enterprise Security & Compliance Review
    t3 = """Sarah Connor: Rachel, thank you for leading our SOC2 compliance audit preparation. What are our core action items?
Rachel Green: We need to enforce strict JWT token rotation, ensure TLS 1.3 across all WebSocket streams, and verify that transcript recordings are encrypted at rest with AES-256.
David Chen: Our database models already support encrypted storage fields. Action item: David will enable AES-256 field encryption on transcripts by Friday.
Rachel Green: Decision: We will require 7-day JWT expiration with automated refresh tokens for all enterprise accounts.
Sarah Connor: Excellent. Action item: Sarah will update the customer data retention policy documentation by Oct 24."""

    m3 = Meeting(
        user_id=user.id,
        title="Enterprise Security & Compliance Review",
        date="2025-10-08",
        duration_minutes=50,
        meeting_type="Security",
        participants=json.dumps(["Sarah Connor", "Rachel Green", "David Chen"]),
        raw_transcript=t3,
        executive_summary="Reviewed SOC2 compliance checklist and enterprise data privacy policies. Reached consensus on mandatory 7-day JWT token rotation and AES-256 encryption at rest for meeting transcripts and audio files. Assigned security hardening tasks to David and policy documentation to Sarah.",
        key_points=json.dumps([
            "Mandated 7-day JWT expiration with automatic refresh rotation.",
            "Enforced AES-256 encryption at rest for raw transcripts.",
            "Established SOC2 compliance audit timeline for Q4."
        ]),
        sentiment="Productive & Strategic",
        tags=json.dumps(["Enterprise Security", "Compliance", "Architecture"])
    )
    db.add(m3)
    db.commit()
    db.refresh(m3)

    for c in chunk_transcript(t3):
        db.add(MeetingChunk(
            meeting_id=m3.id,
            chunk_index=c["chunk_index"],
            speaker=c["speaker"],
            timestamp_str=c["timestamp_str"],
            content=c["content"]
        ))

    d3_1 = Decision(
        meeting_id=m3.id,
        title="Mandate 7-day JWT token rotation and AES-256 transcript encryption",
        rationale="Fulfills enterprise SOC2 compliance standards and guarantees customer data confidentiality.",
        impact="High",
        decision_maker="Rachel Green & Sarah Connor"
    )
    db.add(d3_1)

    # Sample Meeting 4: National AI Hackathon Kickoff & Architecture Alignment
    t4 = """Sarah Connor: Welcome everyone to the AI Hackathon planning sync! Our goal is to build the definitive AI Meeting Assistant: MeetBuddy AI.
Elena Rostova: The UI will feature an animated female futuristic AI avatar with natural blinking, mouth lip-sync, floating animation, and a modern glassmorphism aesthetic.
Alex Rivera: The backend will use FastAPI, SQLAlchemy, and a complete RAG pipeline supporting semantic search across transcripts, tasks, and decisions.
Liam Scott: We also need full Kanban task board drag-and-drop, global voice search, and an interactive meeting calendar.
Sarah Connor: Decision: Build MeetBuddy AI with complete production polish, zero mockups, and real AI capabilities.
Alex Rivera: Action item: Alex will connect the ChromaDB and TF-IDF RAG engine with citation links by Wednesday.
Elena Rostova: Action item: Elena will create the dynamic voice waveform component by Thursday."""

    m4 = Meeting(
        user_id=user.id,
        title="National AI Hackathon Kickoff & Architecture Alignment",
        date="2025-10-05",
        duration_minutes=60,
        meeting_type="Hackathon",
        participants=json.dumps(["Sarah Connor", "Alex Rivera", "Elena Rostova", "Liam Scott"]),
        raw_transcript=t4,
        executive_summary="Kicked off the National AI Hackathon project MeetBuddy AI. Defined complete technical and UI/UX design specifications including an animated AI avatar, glassmorphism dashboard, RAG semantic search, Kanban task board, and voice controls. Delegated core AI pipeline and frontend component milestones.",
        key_points=json.dumps([
            "Established full product scope for MeetBuddy AI SaaS.",
            "Designed animated AI assistant avatar with lip-sync and audio waveforms.",
            "Integrated RAG pipeline with semantic vector chunking and source citations.",
            "Built comprehensive task tracking, calendar, and analytics modules."
        ]),
        sentiment="High Energy & Optimistic",
        tags=json.dumps(["Hackathon", "AI Roadmap", "Design Systems", "RAG & Search"])
    )
    db.add(m4)
    db.commit()
    db.refresh(m4)

    for c in chunk_transcript(t4):
        db.add(MeetingChunk(
            meeting_id=m4.id,
            chunk_index=c["chunk_index"],
            speaker=c["speaker"],
            timestamp_str=c["timestamp_str"],
            content=c["content"]
        ))

    d4_1 = Decision(
        meeting_id=m4.id,
        title="Build MeetBuddy AI with complete production polish and real AI RAG engine",
        rationale="Positions product as a startup-ready SaaS capable of winning national AI competitions.",
        impact="High",
        decision_maker="Sarah Connor"
    )
    db.add(d4_1)

    # Tasks across meetings
    now = datetime.now()
    tasks_data = [
        # Pending Tasks
        {
            "meeting_id": m1.id,
            "title": "Finalize staging deployment configuration for hybrid RAG",
            "description": "Configure Docker swarm and verify 480ms vector retrieval latency benchmarks.",
            "owner": "Alex Rivera",
            "deadline": (now + timedelta(days=2)).strftime("%b %d, %Y"),
            "priority": "High",
            "status": "Pending",
            "completion_percentage": 20
        },
        {
            "meeting_id": m1.id,
            "title": "Draft user onboarding tour with interactive AI avatar",
            "description": "Design step-by-step product walkthrough highlighting meeting uploads and RAG chat.",
            "owner": "Elena Rostova",
            "deadline": (now + timedelta(days=4)).strftime("%b %d, %Y"),
            "priority": "Medium",
            "status": "Pending",
            "completion_percentage": 10
        },
        {
            "meeting_id": m3.id,
            "title": "Update customer data retention policy documentation",
            "description": "Detail AES-256 transcript encryption and 7-day token revocation protocol.",
            "owner": "Sarah Connor",
            "deadline": (now + timedelta(days=6)).strftime("%b %d, %Y"),
            "priority": "Medium",
            "status": "Pending",
            "completion_percentage": 0
        },
        # In Progress Tasks
        {
            "meeting_id": m1.id,
            "title": "Complete security penetration testing on JWT auth middleware",
            "description": "Execute brute-force and token expiration security validation test suites.",
            "owner": "David Chen",
            "deadline": (now + timedelta(days=3)).strftime("%b %d, %Y"),
            "priority": "High",
            "status": "In Progress",
            "completion_percentage": 65
        },
        {
            "meeting_id": m4.id,
            "title": "Connect ChromaDB and TF-IDF RAG engine with citation links",
            "description": "Implement multi-chunk vector ranking and real-time snippet extraction.",
            "owner": "Alex Rivera",
            "deadline": (now + timedelta(days=5)).strftime("%b %d, %Y"),
            "priority": "High",
            "status": "In Progress",
            "completion_percentage": 75
        },
        {
            "meeting_id": m2.id,
            "title": "Implement client-side audio buffering for streaming transcription",
            "description": "Create Web Audio API buffer to handle packet jitter gracefully.",
            "owner": "Marcus Vance",
            "deadline": (now + timedelta(days=7)).strftime("%b %d, %Y"),
            "priority": "Medium",
            "status": "In Progress",
            "completion_percentage": 50
        },
        # Completed Tasks
        {
            "meeting_id": m2.id,
            "title": "Migrate database schemas to PostgreSQL and SQLite fallback",
            "description": "Standardize SQLAlchemy ORM models with thread-safe connection pooling.",
            "owner": "David Chen",
            "deadline": (now - timedelta(days=2)).strftime("%b %d, %Y"),
            "priority": "High",
            "status": "Completed",
            "completion_percentage": 100
        },
        {
            "meeting_id": m4.id,
            "title": "Create dynamic voice waveform and female AI avatar animations",
            "description": "Built interactive SVG canvas with natural eye blinking and audio reactivity.",
            "owner": "Elena Rostova",
            "deadline": (now - timedelta(days=3)).strftime("%b %d, %Y"),
            "priority": "High",
            "status": "Completed",
            "completion_percentage": 100
        },
        {
            "meeting_id": m3.id,
            "title": "Enable AES-256 field encryption for raw transcripts",
            "description": "Applied cryptographically secure cipher routines for encrypted storage at rest.",
            "owner": "David Chen",
            "deadline": (now - timedelta(days=4)).strftime("%b %d, %Y"),
            "priority": "High",
            "status": "Completed",
            "completion_percentage": 100
        }
    ]

    for t_data in tasks_data:
        db.add(Task(
            user_id=user.id,
            meeting_id=t_data["meeting_id"],
            title=t_data["title"],
            description=t_data["description"],
            owner=t_data["owner"],
            deadline=t_data["deadline"],
            priority=t_data["priority"],
            status=t_data["status"],
            completion_percentage=t_data["completion_percentage"]
        ))

    # Notifications
    notifications_data = [
        {"title": "Upcoming Deadline Alert", "message": "Alex Rivera has a milestone due in 48 hours: 'Finalize staging deployment configuration'.", "type": "reminder"},
        {"title": "AI Meeting Processed", "message": "'Q4 Product Strategy & AI Integration Roadmap' was indexed with 4 action items and 2 decisions.", "type": "success"},
        {"title": "Security Verification Passed", "message": "AES-256 transcript encryption confirmed active for all enterprise meetings.", "type": "info"},
    ]
    for n in notifications_data:
        db.add(Notification(user_id=user.id, title=n["title"], message=n["message"], type=n["type"]))

    # Activity Logs
    activities = [
        {"action": "Extracted 3 Action Items", "target": "Q4 Product Strategy Sync", "details": "Assigned to Alex Rivera, David Chen, Elena Rostova"},
        {"action": "Indexed Semantic Chunks", "target": "Sprint 34 Retrospective", "details": "4 chunks indexed into vector memory"},
        {"action": "RAG Chat Consultation", "target": "AI Assistant Avatar", "details": "Answered query on vector caching latency"},
        {"action": "Updated Task Status", "target": "Database Migration", "details": "Moved from In Progress to Completed (100%)"},
    ]
    for act in activities:
        db.add(ActivityLog(user_id=user.id, action=act["action"], target=act["target"], details=act["details"]))

    db.commit()

from sqlalchemy.orm import Session
from app.models import Report, AIAnalysis
from app.core.config import settings
import httpx
import json
import time


class ReportService:
    def __init__(self, db: Session):
        self.db = db

    async def trigger_ai_analysis(self, report: Report) -> None:
        if not settings.OPENAI_API_KEY:
            return

        start_time = time.time()

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": settings.OPENAI_MODEL,
                        "messages": [
                            {
                                "role": "system",
                                "content": """You are an AI assistant for FloodWatch, a flood monitoring system.
Analyze flood reports and extract structured information.

Return JSON with:
- hazard_type: flood, landslide, storm, or other
- hazard_category: specific type like flash_flood, river_flood, etc
- severity: low, medium, high, critical (based on keywords like 'severe', 'danger', 'emergency')
- confidence: 0.0 to 1.0
- summary: 2-3 sentence summary
- entities: {locations: [], population_affected: number, infrastructure: []}"""
                            },
                            {
                                "role": "user",
                                "content": f"Analyze this report:\n{report.raw_text}"
                            }
                        ],
                        "response_format": {"type": "json_object"}
                    }
                )

                if response.status_code == 200:
                    data = response.json()
                    content = data["choices"][0]["message"]["content"]
                    result = json.loads(content)

                    processing_time = int((time.time() - start_time) * 1000)

                    analysis = AIAnalysis(
                        report_id=report.id,
                        hazard_type=result.get("hazard_type", "flood"),
                        hazard_category=result.get("hazard_category"),
                        severity=result.get("severity", "medium"),
                        confidence=float(result.get("confidence", 0.5)),
                        entities=result.get("entities", {}),
                        summary=result.get("summary"),
                        model_version=settings.OPENAI_MODEL,
                        processing_time_ms=processing_time
                    )

                    self.db.add(analysis)
                    report.status = "analyzed"
                    self.db.commit()

        except Exception as e:
            print(f"AI analysis failed: {e}")
            report.status = "pending"
            self.db.commit()
"""
Web API Placeholder Tool
Gelecekteki API entegrasyonu için şablon tool
"""

from typing import Dict, Any
from .base_tool import BaseTool

class WebAPIPlaceholderTool(BaseTool):
    """Gelecekteki web API entegrasyonu için placeholder tool"""
    
    def __init__(self):
        super().__init__(
            name="web_api_integration",
            description="Üniversite web sistemi API entegrasyonu (şu anda pasif)",
            input_schema={
                "type": "object",
                "properties": {
                    "api_endpoint": {
                        "type": "string",
                        "enum": [
                            "student_info",
                            "grades",
                            "course_registration",
                            "academic_calendar",
                            "announcements",
                            "document_request",
                            "exam_schedule",
                            "fee_payment",
                            "dormitory_info",
                            "library_services"
                        ],
                        "description": "API endpoint türü"
                    },
                    "student_id": {
                        "type": "string",
                        "description": "Öğrenci ID/numarası"
                    },
                    "semester": {
                        "type": "string",
                        "description": "Akademik dönem"
                    },
                    "parameters": {
                        "type": "object",
                        "description": "API'ye gönderilecek ek parametreler",
                        "additionalProperties": True
                    }
                },
                "required": ["api_endpoint"]
            }
        )
        
        # Gelecekteki API yapılandırması
        self.api_config = {
            "base_url": "https://api.mcbu.edu.tr/student-affairs/v1",
            "api_key": None,  # Çevre değişkeninden alınacak
            "timeout": 30,
            "retry_count": 3
        }
        
        # Mock API responses - gerçek API geldiğinde kaldırılacak
        self.mock_responses = {
            "student_info": {
                "status": "success",
                "data": {
                    "student_no": "202012345",
                    "name": "Ahmet Yılmaz",
                    "faculty": "Mühendislik Fakültesi",
                    "department": "Bilgisayar Mühendisliği",
                    "year": 4,
                    "gpa": 3.42,
                    "advisor": "Dr. Öğr. Üyesi Zeynep ÇİPİLOĞLU YILDIZ"
                }
            },
            "grades": {
                "status": "success", 
                "data": {
                    "semester": "2024-2025 Güz",
                    "courses": [
                        {
                            "course_code": "BM401",
                            "course_name": "Bitirme Projesi I",
                            "grade": "AA",
                            "credit": 4
                        },
                        {
                            "course_code": "BM411",
                            "course_name": "Yazılım Mühendisliği",
                            "grade": "BA",
                            "credit": 3
                        }
                    ],
                    "semester_gpa": 3.65,
                    "cumulative_gpa": 3.42
                }
            },
            "course_registration": {
                "status": "success",
                "data": {
                    "registration_period": {
                        "start_date": "2025-01-15",
                        "end_date": "2025-01-25"
                    },
                    "available_courses": [
                        {
                            "course_code": "BM402",
                            "course_name": "Bitirme Projesi II",
                            "credit": 4,
                            "quota": 150,
                            "enrolled": 127
                        }
                    ],
                    "registered_courses": []
                }
            },
            "academic_calendar": {
                "status": "success",
                "data": {
                    "current_semester": "2024-2025 Bahar",
                    "important_dates": [
                        {
                            "event": "Dönem Başlangıcı",
                            "date": "2025-02-10"
                        },
                        {
                            "event": "Vize Sınavları",
                            "date": "2025-04-07 - 2025-04-18"
                        },
                        {
                            "event": "Final Sınavları", 
                            "date": "2025-05-26 - 2025-06-06"
                        }
                    ]
                }
            },
            "announcements": {
                "status": "success",
                "data": {
                    "announcements": [
                        {
                            "id": 1,
                            "title": "2024-2025 Bahar Dönemi Ders Kayıtları",
                            "content": "Ders kayıt işlemleri 15-25 Ocak tarihleri arasında yapılacaktır.",
                            "date": "2025-01-10",
                            "category": "akademik"
                        },
                        {
                            "id": 2,
                            "title": "Kütüphane Yaz Çalışma Saatleri",
                            "content": "Yaz döneminde kütüphane 08:00-18:00 saatleri arasında açık olacaktır.",
                            "date": "2025-01-08",
                            "category": "genel"
                        }
                    ]
                }
            }
        }
    
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """API işlemini simüle et (placeholder)"""
        api_endpoint = kwargs.get("api_endpoint")
        student_id = kwargs.get("student_id")
        semester = kwargs.get("semester")
        parameters = kwargs.get("parameters", {})
        
        # Şu anda gerçek API yok, mock response dön
        if api_endpoint in self.mock_responses:
            mock_data = self.mock_responses[api_endpoint].copy()
            
            # Student ID varsa mock data'ya ekle
            if student_id:
                mock_data["request_info"] = {
                    "student_id": student_id,
                    "requested_endpoint": api_endpoint
                }
            
            # Semester varsa mock data'ya ekle
            if semester:
                if "data" in mock_data:
                    mock_data["data"]["requested_semester"] = semester
            
            return self.create_success_response(
                data={
                    "api_status": "MOCK_MODE",
                    "message": "Bu tool henüz aktif değil. Gerçek API entegrasyonu için geliştirme aşamasında.",
                    "future_capabilities": self._get_future_capabilities(),
                    "mock_response": mock_data,
                    "integration_plan": self._get_integration_plan()
                },
                message=f"Mock API response for {api_endpoint}"
            )
        
        else:
            return self.create_error_response(
                f"Bilinmeyen API endpoint: {api_endpoint}",
                "UNKNOWN_ENDPOINT"
            )
    
    def _get_future_capabilities(self) -> Dict[str, Any]:
        """Gelecekteki yetenekleri açıkla"""
        return {
            "planned_features": [
                "Gerçek zamanlı öğrenci bilgi sorgulama",
                "Ders kayıt işlemleri",
                "Not sorgulama ve transkript alma",
                "Sınav programı ve sonuçları",
                "Belge talep işlemleri",
                "Ücret ödeme durumu",
                "Duyuru ve önemli tarihler",
                "Yurt başvuru ve işlemleri",
                "Kütüphane hizmetleri entegrasyonu",
                "Staj başvuru ve takip sistemi"
            ],
            "technical_requirements": [
                "Üniversite API anahtarı",
                "OAuth2 veya JWT token sistemi",
                "SSL/TLS güvenli bağlantı",
                "Rate limiting ve error handling",
                "Veri şifreleme ve güvenlik protokolleri"
            ],
            "integration_timeline": {
                "phase_1": "API dokümantasyonu ve test ortamı hazırlığı",
                "phase_2": "Temel işlevlerin geliştirilmesi (öğrenci bilgi, notlar)",
                "phase_3": "İleri düzey işlevler (kayıt, ödeme, belge talepleri)",
                "phase_4": "Güvenlik testleri ve prodüksiyon hazırlığı"
            }
        }
    
    def _get_integration_plan(self) -> Dict[str, Any]:
        """Entegrasyon planını açıkla"""
        return {
            "current_status": "Placeholder/Mock Mode",
            "next_steps": [
                "Üniversite IT departmanı ile görüşme",
                "API dokümantasyonu alma",
                "Test endpoint'leri belirleme",
                "Güvenlik protokolleri kurma",
                "Pilot test uygulaması geliştirme"
            ],
            "dependencies": [
                "Üniversite web sistemi API desteği",
                "API erişim izinleri",
                "Güvenlik sertifikaları",
                "Test ortamı kurulumu"
            ],
            "estimated_development_time": "2-3 ay (API hazır olduktan sonra)",
            "contact_info": {
                "responsible_department": "Bilgi İşlem Daire Başkanlığı",
                "suggested_contact": "MCBU IT Department"
            }
        }
    
    async def simulate_api_call(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Gelecekteki API çağrısını simüle et"""
        return {
            "simulated_request": {
                "url": f"{self.api_config['base_url']}/{endpoint}",
                "method": "POST",
                "headers": {
                    "Authorization": "Bearer [API_KEY]",
                    "Content-Type": "application/json"
                },
                "data": data
            },
            "simulated_response": {
                "status_code": 200,
                "response_time": "~500ms",
                "data": self.mock_responses.get(endpoint, {"message": "Endpoint not configured"})
            },
            "note": "Bu simülasyon gerçek API çağrısı değildir"
        }
    
    def get_api_documentation(self) -> Dict[str, Any]:
        """API dokümantasyonu şablonu"""
        return {
            "api_name": "MCBU Student Affairs API",
            "version": "v1 (planned)",
            "base_url": self.api_config["base_url"],
            "authentication": "API Key + OAuth2",
            "endpoints": {
                "GET /student/{id}": "Öğrenci bilgilerini getir",
                "GET /student/{id}/grades": "Öğrenci notlarını getir",
                "POST /student/{id}/course-registration": "Ders kaydı yap",
                "GET /academic-calendar": "Akademik takvimi getir",
                "GET /announcements": "Duyuruları getir",
                "POST /document-request": "Belge talebi oluştur",
                "GET /exam-schedule": "Sınav programını getir",
                "GET /fee-status/{id}": "Ücret durumunu getir",
                "GET /dormitory/{id}": "Yurt bilgilerini getir",
                "GET /library/services": "Kütüphane hizmetlerini getir"
            },
            "response_format": {
                "success": {
                    "status": "success",
                    "data": {},
                    "timestamp": "ISO 8601",
                    "request_id": "unique_id"
                },
                "error": {
                    "status": "error",
                    "error_code": "ERROR_CODE",
                    "message": "Error description",
                    "timestamp": "ISO 8601",
                    "request_id": "unique_id"
                }
            },
            "rate_limits": {
                "requests_per_minute": 60,
                "requests_per_hour": 1000,
                "requests_per_day": 10000
            },
            "security": {
                "authentication_required": True,
                "encryption": "TLS 1.3",
                "data_privacy": "KVKK compliant",
                "audit_logging": "Full request/response logging"
            }
        }
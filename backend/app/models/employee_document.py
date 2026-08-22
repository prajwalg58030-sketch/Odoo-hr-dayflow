from app.config.database import db
from datetime import datetime

class EmployeeDocument(db.Model):
    __tablename__ = 'employee_documents'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    document_name = db.Column(db.String(100), nullable=False)
    document_type = db.Column(db.String(50), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'document_name': self.document_name,
            'document_type': self.document_type,
            'file_path': self.file_path,
            'uploaded_at': self.uploaded_at.isoformat() if self.uploaded_at else None
        }
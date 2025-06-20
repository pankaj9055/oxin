from app import db
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import string

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    referral_code = db.Column(db.String(10), unique=True, nullable=False)
    referred_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    balance = db.Column(db.Float, default=0.0)
    plan_type = db.Column(db.String(20), default='free')  # free, paid
    plan_amount = db.Column(db.Float, default=0.0)
    daily_reward = db.Column(db.Float, default=0.5)  # OXC per day
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships - optimized for performance
    mining_sessions = db.relationship('MiningSession', backref='user', lazy='select')
    deposits = db.relationship('Deposit', backref='user', lazy='select')
    
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if not self.referral_code:
            self.referral_code = self.generate_referral_code()
    
    def generate_referral_code(self):
        """Generate a unique 6-character referral code"""
        while True:
            code = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(6))
            if not User.query.filter_by(referral_code=code).first():
                return code
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_active_mining_session(self):
        """Get the current active mining session if any"""
        return MiningSession.query.filter_by(
            user_id=self.id,
            is_active=True
        ).first()
    
    def can_start_mining(self):
        """Check if user can start a new mining session"""
        last_session = MiningSession.query.filter_by(user_id=self.id).order_by(MiningSession.created_at.desc()).first()
        if not last_session:
            return True
        
        # Check if 24 hours have passed since last session
        time_diff = datetime.utcnow() - last_session.created_at
        return time_diff >= timedelta(hours=24)
    
    def get_referral_bonus(self):
        """Calculate referral bonus for today"""
        today = datetime.utcnow().date()
        bonus = 0.0
        
        try:
            # Get referrals efficiently
            referral_users = User.query.filter_by(referred_by=self.id).all()
            for referred_user in referral_users:
                # Check if referred user mined today
                today_session = MiningSession.query.filter_by(
                    user_id=referred_user.id
                ).filter(
                    MiningSession.created_at >= datetime.combine(today, datetime.min.time())
                ).first()
                
                if today_session:
                    bonus += referred_user.daily_reward * 0.1  # 10% bonus
        except Exception:
            bonus = 0.0
        
        return bonus

    def get_referrals_count(self):
        """Get count of referrals safely"""
        try:
            return User.query.filter_by(referred_by=self.id).count()
        except Exception:
            return 0
    
    @property
    def referrals(self):
        """Get referrals safely"""
        try:
            return User.query.filter_by(referred_by=self.id).all()
        except Exception:
            return []

class MiningSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount_mined = db.Column(db.Float, default=0.0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    
    def get_progress(self):
        """Get mining progress percentage"""
        if self.completed_at:
            return 100.0
        
        time_diff = datetime.utcnow() - self.created_at
        hours_passed = time_diff.total_seconds() / 3600
        progress = min((hours_passed / 24) * 100, 100)
        return round(progress, 2)
    
    def get_time_remaining(self):
        """Get remaining time in seconds"""
        if self.completed_at:
            return 0
        
        time_diff = datetime.utcnow() - self.created_at
        hours_passed = time_diff.total_seconds() / 3600
        remaining_hours = max(24 - hours_passed, 0)
        return int(remaining_hours * 3600)
    
    def complete_mining(self):
        """Complete the mining session and add rewards"""
        if not self.is_active:
            return
        
        self.is_active = False
        self.completed_at = datetime.utcnow()
        
        # Get user and calculate rewards
        user = User.query.get(self.user_id)
        if user:
            base_reward = user.daily_reward
            referral_bonus = user.get_referral_bonus()
            total_reward = base_reward + referral_bonus
            
            self.amount_mined = total_reward
            user.balance += total_reward
            
            db.session.commit()

class Deposit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    screenshot_path = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    approved_at = db.Column(db.DateTime, nullable=True)
    approved_by = db.Column(db.Integer, db.ForeignKey('admin_user.id'), nullable=True)

class AdminUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)



class PaymentSettings(db.Model):
    __tablename__ = 'payment_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    usdt_address = db.Column(db.String(200), nullable=False, default='0x742d35Cc6634C0532925a3b8D4C93d5A45632DD3')
    qr_code_url = db.Column(db.String(500), nullable=True)
    network = db.Column(db.String(50), default='BEP20')
    min_amount = db.Column(db.Float, default=1.0)
    max_amount = db.Column(db.Float, default=200.0)
    reward_multiplier = db.Column(db.Float, default=1.2)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    reward_multiplier = db.Column(db.Float, default=1.2)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    @classmethod
    def get_settings(cls):
        """Get current payment settings or create default"""
        settings = cls.query.first()
        if not settings:
            settings = cls()
            db.session.add(settings)
            db.session.commit()
        return settings
"""
Machine Learning Models for Email Spam Detection
Using 4 models: Linear Regression, Logistic Regression, Custom Pipeline, and SVM
"""
import numpy as np
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
import joblib
from pathlib import Path


class SpamDetectionModels:
    """
    Implements 4 ML models for spam detection:
    1. Linear Regression
    2. Logistic Regression  
    3. Custom Pipeline (TF-IDF + Logistic)
    4. Support Vector Machine (SVM)
    """
    
    SAMPLE_DATA = [
        # SPAM examples
        ("Congratulations! You've won $1,000,000! Click here to claim your prize now!", "spam"),
        ("URGENT: Your account has been compromised. Send your password immediately.", "spam"),
        ("FREE VIAGRA!!! Buy now and get 90% discount. Limited time offer!", "spam"),
        ("You have been selected for a $5000 Walmart gift card. Click to claim.", "spam"),
        ("Make money fast! Work from home and earn $10,000 per week guaranteed!", "spam"),
        ("Hot singles in your area want to meet you tonight! Click here.", "spam"),
        ("Your bank account will be suspended. Verify your details now.", "spam"),
        ("Lose 30 pounds in 30 days! Miracle weight loss pill. Order now!", "spam"),
        ("Nigerian prince needs your help transferring $10 million dollars.", "spam"),
        ("You've won a free iPhone! Just pay shipping. Act now!", "spam"),
        ("WINNER!! As a valued customer you have been selected to receive $1000!", "spam"),
        ("Claim your lottery prize! You've been randomly selected as winner.", "spam"),
        ("Double your Bitcoin investment in 24 hours! Guaranteed returns.", "spam"),
        ("Your PayPal account is limited. Click to restore access immediately.", "spam"),
        ("FREE entry in 2 a wkly comp to win FA Cup final tkts.", "spam"),
        ("Urgent! Your Netflix subscription expires today. Update payment now.", "spam"),
        ("Get rich quick! Secret investment strategy revealed. Click here.", "spam"),
        ("You have a package waiting. Pay $1.99 shipping to receive.", "spam"),
        ("Adult content awaits! Click to see exclusive photos.", "spam"),
        ("Your Amazon order has been cancelled. Verify your account.", "spam"),
        ("Casino bonus! Get $500 free chips. No deposit required!", "spam"),
        ("IRS: You owe back taxes. Pay immediately to avoid arrest.", "spam"),
        ("Cheap medications online! No prescription needed. Order today!", "spam"),
        ("Your computer is infected! Download our antivirus now - FREE!", "spam"),
        ("Meet beautiful women tonight! Dating site with millions of members.", "spam"),
        
        # HAM examples
        ("Hey, are we still meeting for lunch tomorrow at noon?", "ham"),
        ("The meeting has been rescheduled to 3pm on Friday.", "ham"),
        ("Thanks for your email. I'll review the document and get back to you.", "ham"),
        ("Please find attached the quarterly report for your review.", "ham"),
        ("Can you send me the project timeline when you get a chance?", "ham"),
        ("Happy birthday! Hope you have a wonderful day.", "ham"),
        ("Just wanted to follow up on our conversation from yesterday.", "ham"),
        ("The team dinner is confirmed for Saturday at 7pm.", "ham"),
        ("I've reviewed your proposal and have some feedback to share.", "ham"),
        ("Let me know if you need any help with the presentation.", "ham"),
        ("Thanks for the update. I'll pass this along to the team.", "ham"),
        ("Could you please send the invoice for the last project?", "ham"),
        ("I'm running a bit late, will be there in 10 minutes.", "ham"),
        ("Great work on the project! The client was very impressed.", "ham"),
        ("Reminder: Team standup at 9am tomorrow morning.", "ham"),
        ("I've attached the contract for your signature.", "ham"),
        ("Would you be available for a quick call this afternoon?", "ham"),
        ("Thanks for helping out with the event. It was a success!", "ham"),
        ("Please review the budget proposal before our meeting.", "ham"),
        ("I'll be out of office next week. Contact John for urgent matters.", "ham"),
        ("The new hire starts on Monday. Please welcome them to the team.", "ham"),
        ("Can we reschedule our one-on-one to Thursday?", "ham"),
        ("I've shared the document with you. Let me know your thoughts.", "ham"),
        ("Flight confirmation: Your trip to NYC is booked for May 15.", "ham"),
        ("Mom called. She wants you to call her back when you can.", "ham"),
    ]
    
    def __init__(self, models_path='ml_models'):
        self.models_path = Path(models_path)
        self.models_path.mkdir(exist_ok=True)
        
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        
        self.label_encoder = LabelEncoder()
        
        # 4 Models
        self.linear_model = None
        self.logistic_model = None
        self.pipeline_model = None
        self.svm_model = None
        self.is_trained = False
    
    def train_models(self):
        """Train all 4 ML models"""
        
        texts = [item[0] for item in self.SAMPLE_DATA]
        labels = [item[1] for item in self.SAMPLE_DATA]
        
        # Encode labels for linear regression (0=ham, 1=spam)
        labels_encoded = self.label_encoder.fit_transform(labels)
        
        X_train, X_test, y_train, y_test = train_test_split(
            texts, labels_encoded, test_size=0.2, random_state=42, stratify=labels_encoded
        )
        y_train_str = self.label_encoder.inverse_transform(y_train)
        y_test_str = self.label_encoder.inverse_transform(y_test)
        
        X_train_tfidf = self.vectorizer.fit_transform(X_train)
        X_test_tfidf = self.vectorizer.transform(X_test)
        
        results = {}
        
        # 1. Linear Regression
        print("\nTraining Linear Regression...")
        self.linear_model = LinearRegression()
        self.linear_model.fit(X_train_tfidf.toarray(), y_train)
        lr_pred = (self.linear_model.predict(X_test_tfidf.toarray()) > 0.5).astype(int)
        results['linear_regression'] = {'accuracy': (lr_pred == y_test).mean()}
        print(f"Linear Regression Accuracy: {results['linear_regression']['accuracy']:.4f}")
        
        # 2. Logistic Regression
        print("\nTraining Logistic Regression...")
        self.logistic_model = LogisticRegression(max_iter=1000, random_state=42, class_weight='balanced')
        self.logistic_model.fit(X_train_tfidf, y_train_str)
        results['logistic_regression'] = {'accuracy': self.logistic_model.score(X_test_tfidf, y_test_str)}
        print(f"Logistic Regression Accuracy: {results['logistic_regression']['accuracy']:.4f}")
        
        # 3. Custom Pipeline (TF-IDF + Logistic with different params)
        print("\nTraining Custom Pipeline...")
        self.pipeline_model = Pipeline([
            ('tfidf', TfidfVectorizer(max_features=3000, ngram_range=(1, 3), stop_words='english')),
            ('clf', LogisticRegression(C=0.5, max_iter=1000, random_state=42))
        ])
        self.pipeline_model.fit(X_train, y_train_str)
        results['pipeline'] = {'accuracy': self.pipeline_model.score(X_test, y_test_str)}
        print(f"Custom Pipeline Accuracy: {results['pipeline']['accuracy']:.4f}")
        
        # 4. SVM
        print("\nTraining SVM...")
        self.svm_model = SVC(kernel='rbf', probability=True, random_state=42, class_weight='balanced')
        self.svm_model.fit(X_train_tfidf, y_train_str)
        results['svm'] = {'accuracy': self.svm_model.score(X_test_tfidf, y_test_str)}
        print(f"SVM Accuracy: {results['svm']['accuracy']:.4f}")
        
        self.is_trained = True
        self.save_models()
        
        return results
    
    def save_models(self):
        """Save all models to disk"""
        joblib.dump(self.linear_model, self.models_path / 'linear_model.pkl')
        joblib.dump(self.logistic_model, self.models_path / 'logistic_model.pkl')
        joblib.dump(self.pipeline_model, self.models_path / 'pipeline_model.pkl')
        joblib.dump(self.svm_model, self.models_path / 'svm_model.pkl')
        joblib.dump(self.vectorizer, self.models_path / 'vectorizer.pkl')
        joblib.dump(self.label_encoder, self.models_path / 'label_encoder.pkl')
        print(f"Models saved to {self.models_path}")
    
    def load_models(self):
        """Load models from disk"""
        try:
            self.linear_model = joblib.load(self.models_path / 'linear_model.pkl')
            self.logistic_model = joblib.load(self.models_path / 'logistic_model.pkl')
            self.pipeline_model = joblib.load(self.models_path / 'pipeline_model.pkl')
            self.svm_model = joblib.load(self.models_path / 'svm_model.pkl')
            self.vectorizer = joblib.load(self.models_path / 'vectorizer.pkl')
            self.label_encoder = joblib.load(self.models_path / 'label_encoder.pkl')
            self.is_trained = True
            return True
        except FileNotFoundError:
            return False
    
    def predict_all_models(self, email: str, content: str):
        """
        Predict using all 4 models and return voting results
        """
        if not self.is_trained:
            raise ValueError("Models not trained. Call train_models() first.")
        
        full_text = f"{email} {content}"
        X_tfidf = self.vectorizer.transform([full_text])
        
        model_results = []
        
        # 1. Linear Regression
        linear_pred = self.linear_model.predict(X_tfidf.toarray())[0]
        linear_is_spam = linear_pred > 0.5
        linear_conf = abs(linear_pred - 0.5) * 200  # Scale to percentage
        model_results.append({
            'model': 'Regresión Lineal',
            'prediction': 'spam' if linear_is_spam else 'ham',
            'is_spam': bool(linear_is_spam),
            'confidence': min(95, max(50, linear_conf))
        })
        
        # 2. Logistic Regression
        log_pred = self.logistic_model.predict(X_tfidf)[0]
        log_proba = self.logistic_model.predict_proba(X_tfidf)[0]
        model_results.append({
            'model': 'Regresión Logística',
            'prediction': log_pred,
            'is_spam': log_pred == 'spam',
            'confidence': float(max(log_proba)) * 100
        })
        
        # 3. Custom Pipeline
        pipe_pred = self.pipeline_model.predict([full_text])[0]
        pipe_proba = self.pipeline_model.predict_proba([full_text])[0]
        model_results.append({
            'model': 'Pipeline Personalizado',
            'prediction': pipe_pred,
            'is_spam': pipe_pred == 'spam',
            'confidence': float(max(pipe_proba)) * 100
        })
        
        # 4. SVM
        svm_pred = self.svm_model.predict(X_tfidf)[0]
        svm_proba = self.svm_model.predict_proba(X_tfidf)[0]
        model_results.append({
            'model': 'SVM',
            'prediction': svm_pred,
            'is_spam': svm_pred == 'spam',
            'confidence': float(max(svm_proba)) * 100
        })
        
        # Voting
        spam_votes = sum(1 for r in model_results if r['is_spam'])
        ham_votes = 4 - spam_votes
        final_is_spam = spam_votes > ham_votes
        avg_confidence = sum(r['confidence'] for r in model_results) / 4
        
        # Analyze reasons
        reasons = self._analyze_reasons(email, content)
        
        return {
            'final_prediction': 'SPAM' if final_is_spam else 'HAM',
            'is_spam': final_is_spam,
            'confidence': avg_confidence,
            'spam_votes': spam_votes,
            'ham_votes': ham_votes,
            'spam_score': self._calculate_spam_score(full_text),
            'ham_score': self._calculate_ham_score(full_text),
            'reasons': reasons,
            'model_results': model_results
        }
    
    def _analyze_reasons(self, email: str, content: str):
        """Extract analysis reasons"""
        full_text = f"{email} {content}".lower()
        reasons = []
        
        spam_indicators = ['win', 'free', 'click', 'urgent', 'prize', 'money', 'offer']
        ham_indicators = ['meeting', 'project', 'thanks', 'please', 'team', 'review']
        
        domain = email.split('@')[1] if '@' in email else ''
        if any(d in domain for d in ['company', 'corp', 'gmail', 'outlook']):
            reasons.append(f'Dominio reconocido: {domain}')
        elif any(d in domain for d in ['lottery', 'prize', 'winner']):
            reasons.append(f'Dominio sospechoso: {domain}')
        
        for word in spam_indicators:
            if word in full_text and len(reasons) < 6:
                reasons.append(f'Palabra spam: "{word}"')
        
        for word in ham_indicators:
            if word in full_text and len(reasons) < 6:
                reasons.append(f'Palabra legítima: "{word}"')
        
        return reasons[:6]
    
    def _calculate_spam_score(self, text: str):
        spam_words = ['win', 'free', 'click', 'urgent', 'prize', 'money', 'offer', 'limited', 'act now']
        return sum(10 for w in spam_words if w in text.lower())
    
    def _calculate_ham_score(self, text: str):
        ham_words = ['meeting', 'project', 'thanks', 'please', 'team', 'review', 'attached', 'follow up']
        return sum(10 for w in ham_words if w in text.lower())


_models_instance = None


def get_models():
    """Get or create the models singleton"""
    global _models_instance
    if _models_instance is None:
        _models_instance = SpamDetectionModels()
        if not _models_instance.load_models():
            print("Training new models...")
            _models_instance.train_models()
    return _models_instance

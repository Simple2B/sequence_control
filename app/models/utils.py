from app import db


class ModelMixin(object):
    def save(self):
        # Save this model to the database.
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self, commit=True):
        """Delete instance"""
        db.session.delete(self)
        if commit:
            db.session.commit()
        return self


# Add your own utility classes and functions here.

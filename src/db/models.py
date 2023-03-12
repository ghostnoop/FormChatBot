from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.postgres.fields import ArrayField


class BaseModel(Model):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Question(BaseModel):
    title = fields.CharField(max_length=255, unique=True)
    answers = ArrayField(element_type='varchar', null=True, default=None)
    is_admin_only = fields.BooleanField(default=False)


class User(BaseModel):
    id = fields.BigIntField(pk=True)
    nickname = fields.CharField(max_length=255, null=True, default=None)


class QuestionForm(BaseModel):
    user = fields.ForeignKeyField('models.User', on_delete='CASCADE')
    is_done = fields.BooleanField(default=False)

    async def get_channel_form_id(self):
        obj = await QuestionFormWithQuestion.get(question_form_id=self.id, question_id=2)
        if obj.answer == 'Женский':
            return f'W{self.id}'
        else:
            return f'M{self.id}'


class QuestionFormWithQuestion(BaseModel):
    question_form = fields.ForeignKeyField('models.QuestionForm', on_delete='CASCADE')
    question = fields.ForeignKeyField('models.Question', on_delete='CASCADE')
    answer = fields.CharField(max_length=255)

    class Meta:
        unique_together = (("question_form_id", "question_id"),)


class Fixture(BaseModel):
    name = fields.CharField(max_length=255)


_models = {"Question": Question, "User": User, "Fixture": Fixture,
           "QuestionForm": QuestionForm, "QuestionFormWithQuestion": QuestionFormWithQuestion}

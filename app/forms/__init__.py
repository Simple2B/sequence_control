# flake8: noqa F401
from .auth import (
    LoginForm,
    RegistrationForm,
    PmRegistrationForm,
    WPMRegistrationForm,
    SelectViewerForm,
    AdminSelectViewerForm,
    EditUserForm,
)
from .project import ProjectForm, ProjectChooseForm
from .reason import ReasonForm
from .wp_milestone import WPMilestoneFrom, MilestoneFrom
from .work_package import WorkPackageForm
from .location import BuildingForm, LevelForm, LocationForm
from .import_file import ImportFileForm

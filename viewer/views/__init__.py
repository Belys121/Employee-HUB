from .HomepageView import HomepageView
from .contract import ContractView, ContractCreateView, ContractUpdateView, ContractDeleteView, ContractListView, ContractAllListView, contract_detail
from .customer import CustomerView, CustomerCreateView, CustomerUpdateView, CustomerDeleteView
from .subcontract import SubContractAllListView, SubContractView, SubContractCreateView, SubContractUpdateView, \
    SubContractDeleteView, SubContractDetailView, show_subcontracts, subcontract_detail
from .user import UserListView
from .comment import CommentListView, CommentCreateView
from .calendar import calendar_view, events_feed, create_event, get_groups, update_event, delete_event
from .employeeProfile import employee_profile, change_security_question_view
from .singup_login_passwordchange import SignUpView, SubmittableLoginView, SubmittablePasswordChangeView
from .password_reset import password_reset_step_1, password_reset_step_2, password_reset_step_3
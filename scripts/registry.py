from dataclasses import dataclass


@dataclass(frozen=True)
class ScriptEntry:
    filename: str
    category: str
    title: str
    description: str
    notes: str = ""
    requires_account_code: bool = False

    @property
    def command_name(self):
        return self.filename[:-3] if self.filename.endswith(".py") else self.filename


SCRIPT_REGISTRY = (
    ScriptEntry(
        "get_account.py",
        "Account & Identity",
        "Account info",
        "Account info and account code discovery.",
        "Add account_code to stored config from output when needed.",
    ),
    ScriptEntry(
        "get_support_info.py",
        "Account & Identity",
        "Support info",
        "Support contacts, renewal date, and package.",
    ),
    ScriptEntry(
        "get_emergency_contact.py",
        "Account & Identity",
        "Emergency contact",
        "Emergency contact details from the v1 API.",
    ),
    ScriptEntry(
        "get_whoami.py",
        "Account & Identity",
        "Whoami",
        "Identity info for the authenticated caller.",
        "Uses account_code header when present.",
    ),
    ScriptEntry(
        "get_dashboard_notifications.py",
        "Account & Identity",
        "Dashboard notifications",
        "Admin dashboard notifications filtered to the last 2 years.",
        "",
        requires_account_code=True,
    ),
    ScriptEntry(
        "get_rejection_logs.py",
        "Gateway - Logs With Time Frames",
        "Rejection logs",
        "Gateway rejection logs.",
        "Prompts for time frame, page size, and pagination.",
    ),
    ScriptEntry(
        "get_held_release_logs.py",
        "Gateway - Logs With Time Frames",
        "Held/release logs",
        "Held and release action logs.",
        "Prompts for time frame, page size, and pagination.",
    ),
    ScriptEntry(
        "get_hold_message_list.py",
        "Gateway - Logs With Time Frames",
        "Held message list",
        "Currently-held messages.",
        "Prompts for time frame, page size, admin y/n, and pagination.",
    ),
    ScriptEntry(
        "get_audit_events.py",
        "Gateway - Logs With Time Frames",
        "Audit events",
        "Audit events with a 60-day option.",
        "Prompts for time frame, page size, and pagination.",
    ),
    ScriptEntry(
        "get_hold_summary_list.py",
        "Gateway - Other",
        "Hold summary",
        "Counts of currently held messages grouped by policy.",
        "Aggregate output.",
    ),
    ScriptEntry(
        "get_email_queues.py",
        "Gateway - Other",
        "Email queues",
        "Inbound and outbound queue depth over the last 24 hours.",
        "Aggregate output.",
    ),
    ScriptEntry(
        "get_gateway_details.py",
        "Gateway - Other",
        "Gateway details",
        "Cloud Gateway outbound config, mail platforms, SPF, and MX details.",
    ),
    ScriptEntry(
        "get_outbound_ip_addresses.py",
        "Gateway - Other",
        "Outbound IP addresses",
        "Configured outbound IP addresses for the account mail platform.",
    ),
    ScriptEntry(
        "get_email_statistics.py",
        "Gateway - Other",
        "Email statistics",
        "Cloud Gateway email statistics and delivery health.",
    ),
    ScriptEntry(
        "get_dlp_logs.py",
        "DLP & TTP Logs",
        "DLP logs",
        "DLP event logs.",
        "Prompts for time frame, page size, and pagination.",
    ),
    ScriptEntry(
        "get_ttp_url_logs.py",
        "DLP & TTP Logs",
        "TTP URL logs",
        "TTP URL click logs.",
        "Prompts for time frame, scan result, route, page size, and pagination.",
    ),
    ScriptEntry(
        "get_ttp_attachment_logs.py",
        "DLP & TTP Logs",
        "TTP attachment logs",
        "TTP attachment protection logs for the last 7 days.",
    ),
    ScriptEntry(
        "get_ttp_impersonation_logs.py",
        "DLP & TTP Logs",
        "TTP impersonation logs",
        "TTP impersonation protection logs for the last 7 days.",
    ),
    ScriptEntry(
        "find_groups.py",
        "Directory & Domains",
        "Find groups",
        "Directory groups.",
        "Prompts for source, optional query, and pagination.",
    ),
    ScriptEntry(
        "get_group_members.py",
        "Directory & Domains",
        "Group members",
        "Group members for a directory group.",
        "Can list groups first, then prompts for group ID.",
    ),
    ScriptEntry(
        "get_internal_domains.py",
        "Directory & Domains",
        "Internal domains",
        "Internal domains on the account.",
    ),
    ScriptEntry(
        "get_internal_users.py",
        "Directory & Domains",
        "Internal users",
        "Internal users for a domain.",
        "Lists internal domains or accepts manual entry, then paginates.",
    ),
    ScriptEntry(
        "get_directory_connections.py",
        "Directory & Domains",
        "Directory connections",
        "Directory connectors configured on the tenant.",
    ),
    ScriptEntry(
        "get_user_aliases.py",
        "Directory & Domains",
        "User aliases",
        "Aliases associated with a primary email address.",
        "Prompts for email address.",
    ),
    ScriptEntry(
        "get_user_attributes.py",
        "Directory & Domains",
        "User attributes",
        "Custom attributes registered for a user.",
        "Prompts for email; can save thumbnailPhoto to current directory.",
    ),
    ScriptEntry(
        "find_delegate_users.py",
        "Directory & Domains",
        "Delegate users",
        "Delegate users for a primary email address.",
        "Prompts for primary address.",
    ),
    ScriptEntry(
        "get_most_used_contacts.py",
        "Directory & Domains",
        "Most-used contacts",
        "Most-used contacts synced from Azure Active Directory.",
    ),
    ScriptEntry(
        "get_all_managed_urls.py",
        "URLs & Archive",
        "Managed URLs",
        "Managed URL list for allow and block entries.",
    ),
    ScriptEntry(
        "get_archive_search_logs.py",
        "URLs & Archive",
        "Archive search logs",
        "Archive search activity logs.",
        "Prints next page token when returned.",
    ),
    ScriptEntry(
        "get_audit_categories.py",
        "URLs & Archive",
        "Audit categories",
        "Available audit event category IDs and names.",
    ),
    ScriptEntry(
        "get_provisioning_packages.py",
        "URLs & Archive",
        "Provisioning packages",
        "Provisioning packages available on the tenant.",
    ),
    ScriptEntry(
        "decode_url.py",
        "URL Decoder",
        "Decode URL",
        "Decode a Mimecast protected URL.",
        "Accepts an argument when run directly; prompts through the launcher.",
    ),
)


def script_lookup():
    entries = {}
    for entry in SCRIPT_REGISTRY:
        entries[entry.filename] = entry
        entries[entry.command_name] = entry
    return entries

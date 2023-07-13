# Script must be run with administrator privileges
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Warning "You do not have Administrator rights to run this script. Please re-run this script as an Administrator!"
    exit
}

# Get all local accounts on the system
$LocalUsers = Get-LocalUser

# Loop through each local user
foreach ($User in $LocalUsers) {

    # Ensure only necessary user accounts have admin privileges
    # This will remove admin privileges for all users except 'necessary_user1' and 'necessary_user2' change these values to your users usernames
    if ($User.Name -ne 'necessary_user1' -and $User.Name -ne 'necessary_user2' -and $User.Enabled -eq $True) {
        Remove-LocalGroupMember -Group "Administrators" -Member $User.Name
        Write-Host "Removed user $($User.Name) from Administrators group"
    }
}

# Disable the Guest account
$GuestAccount = Get-LocalUser -Name "Guest"
if ($GuestAccount.Enabled -eq $True) {
    $GuestAccount | Disable-LocalUser
    Write-Host "Disabled Guest account"
}

# Rename the local administrator account
# Make sure to change New_Admin_Name to your new Admins name.
$AdminAccount = Get-LocalUser -Name "Administrator"
if ($AdminAccount) {
    $AdminAccount | Rename-LocalUser -NewName "New_Admin_Name"
    Write-Host "Renamed Administrator account"
}

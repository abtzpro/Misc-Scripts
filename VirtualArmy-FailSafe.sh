# Define variables for the virtual servers and devices
echo "Welcome to the slave-master data redundancy backup setup script!"
echo "Please enter the name for your master virtual server: "
read master_name
echo "Please enter the name for your slave virtual server: "
read slave_name
echo "Please enter the operating system for your virtual servers: "
read vm_os
echo "Please enter the number of CPUs for your virtual servers: "
read vm_cpu
echo "Please enter the amount of RAM for your virtual servers (in MB): "
read vm_ram

# Define the array of VM names
vms=("$master_name" "$slave_name")

# Define functions to create, start, stop, and delete virtual machines
create_vm() {
  echo "Creating virtual machine $1 with $vm_cpu CPUs, $vm_ram MB of RAM, and $vm_os operating system..."
  VBoxManage createvm --name "$1" --ostype $vm_os --register
  VBoxManage modifyvm "$1" --cpus $vm_cpu --memory $vm_ram --boot1 dvd --boot2 disk --boot3 none --boot4 none
}

start_vm() {
  echo "Starting virtual machine $1..."
  VBoxManage startvm "$1" --type headless
}

stop_vm() {
  echo "Stopping virtual machine $1..."
  VBoxManage controlvm "$1" poweroff
}

delete_vm() {
  echo "Deleting virtual machine $1..."
  VBoxManage unregistervm "$1" --delete
}

# Define the main menu
while true
do
  echo ""
  echo "Please select an option:"
  echo "1. Create virtual machines"
  echo "2. Start virtual machines"
  echo "3. Stop virtual machines"
  echo "4. Delete virtual machines"
  echo "5. Exit"

  read choice

  case $choice in
    1)
      create_vm "$master_name"
      vms+=("$master_name")
      create_vm "$slave_name"
      vms+=("$slave_name")
      ;;
    2)
      echo "Starting virtual machines..."
      for ((i=0; i<${#vms[@]}; i++))
      do
        start_vm "${vms[$i]}"
      done
      ;;
    3)
      echo "Stopping virtual machines..."
      for ((i=0; i<${#vms[@]}; i++))
      do
        stop_vm "${vms[$i]}"
      done
      ;;
    4)
      echo "Deleting virtual machines..."
      for ((i=0; i<${#vms[@]}; i++))
      do
        delete_vm "${vms[$i]}"
      done
      vms=()
      ;;
    5)
      echo "Exiting script..."
      exit 0
      ;;

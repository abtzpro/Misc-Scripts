#!/bin/bash

# Define variables for the virtual servers and devices
echo "Welcome to the virtual server and device spin-up script!"
echo "Please enter the name for your virtual server and device: "
read vm_name
echo "Please enter the operating system for your virtual server and device: "
read vm_os
echo "Please enter the number of CPUs for your virtual server and device: "
read vm_cpu
echo "Please enter the amount of RAM for your virtual server and device (in MB): "
read vm_ram

# Define functions to create, start, stop, and delete virtual machines
create_vm() {
  echo "Creating virtual machine $vm_name$1 with $vm_cpu CPUs, $vm_ram MB of RAM, and $vm_os operating system..."
  VBoxManage createvm --name "$vm_name$1" --ostype $vm_os --register
  VBoxManage modifyvm "$vm_name$1" --cpus $vm_cpu --memory $vm_ram --boot1 dvd --boot2 disk --boot3 none --boot4 none
}

start_vm() {
  echo "Starting virtual machine $vm_name$1..."
  VBoxManage startvm "$vm_name$1" --type headless
}

stop_vm() {
  echo "Stopping virtual machine $vm_name$1..."
  VBoxManage controlvm "$vm_name$1" poweroff
}

delete_vm() {
  echo "Deleting virtual machine $vm_name$1..."
  VBoxManage unregistervm "$vm_name$1" --delete
}

# Define the main menu
while true
do
  echo ""
  echo "Please select an option:"
  echo "1. Create virtual machine"
  echo "2. Start virtual machine"
  echo "3. Stop virtual machine"
  echo "4. Delete virtual machine"
  echo "5. Exit"

  read choice

  case $choice in
    1)
      echo "How many virtual machines do you want to create?"
      read count
      for ((i=1; i<=$count; i++))
      do
        create_vm $i
      done
      ;;
    2)
      echo "Which virtual machine do you want to start?"
      read name
      start_vm $name
      ;;
    3)
      echo "Which virtual machine do you want to stop?"
      read name
      stop_vm $name
      ;;
    4)
      echo "Which virtual machine do you want to delete?"
      read name
      delete_vm $name
      ;;
    5)
      echo "Exiting..."
      exit 0
      ;;
    *)
      echo "Invalid choice. Please try again."
      ;;
  esac
done

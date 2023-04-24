#!/bin/bash

# purpose: Redundancy. Because, what's more frustrating? Having a machine attacked? 
# or being unable to determine why the tango hasn't lost any progress and won't seem to stay down?

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

# Define the array of VM names
vms=("Windows VM 1" "Windows VM 2" "Windows VM 3")

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
        echo "Please enter a name for virtual machine $i:"
        read vm_name
        create_vm "$vm_name"
        vms+=("$vm_name")
      done
      ;;
    2)
      echo "Which virtual machine do you want to start?"
      for ((i=0; i<${#vms[@]}; i++))
      do
        echo "$((i+1)). ${vms[$i]}"
      done
      read index
      start_vm "${vms[$((index-1))]}"
      ;;
    3)
      echo "Which virtual machine do you want to stop?"
      for ((i=0; i<${#vms[@]}; i++))
      do
        echo "$((i+1)). ${vms[$i]}"
      done
      read index
      stop_vm "${vms[$((index-1))]}"
      ;;
    4)
      echo "Which virtual machine do you want to delete?"
      for ((i=0; i<${#vms[@]}; i++))
      do
        echo "$((i+1)). ${vms[$i]}"
      done
      read index
      delete_vm "${vms[$((index-1))]}"
      vms=("${vms[@]:0:$((index-1))}" "${vms[@]:$index

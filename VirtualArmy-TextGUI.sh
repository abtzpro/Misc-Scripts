#!/bin/bash

# Check if VirtualBox is installed
if ! command -v vboxmanage &> /dev/null
then
    echo "VBoxManage is not installed. Installing now..."
    sudo apt-get update
    sudo apt-get install virtualbox
fi

# Text based GUI options for controlling VirtualBox VMs
while true; do
    echo ""
    echo "Please select an option:"
    echo "1. Start VM"
    echo "2. Stop VM"
    echo "3. Restart VM"
    echo "4. List running VMs"
    echo "5. List available VMs"
    echo "6. Create new VM"
    echo "7. Exit"

    read -p "Enter your choice: " choice

    case $choice in
        1)
            read -p "Enter the name of the VM you want to start: " vm_name
            vboxmanage startvm "$vm_name" --type headless
            ;;
        2)
            read -p "Enter the name of the VM you want to stop: " vm_name
            vboxmanage controlvm "$vm_name" poweroff
            ;;
        3)
            read -p "Enter the name of the VM you want to restart: " vm_name
            vboxmanage controlvm "$vm_name" reset
            ;;
        4)
            vboxmanage list runningvms
            ;;
        5)
            vboxmanage list vms
            ;;
        6)
            read -p "Enter the name of the new VM: " vm_name
            read -p "Enter the size of the VM (in MB): " vm_size
            read -p "Enter the number of CPUs for the VM: " vm_cpus
            read -p "Enter the amount of RAM for the VM (in MB): " vm_ram
            read -p "Enter the path to the ISO file: " iso_path
            vboxmanage createvm --name "$vm_name" --register
            vboxmanage modifyvm "$vm_name" --memory "$vm_ram" --cpus "$vm_cpus"
            vboxmanage createhd --filename "$vm_name.vdi" --size "$vm_size"
            vboxmanage storagectl "$vm_name" --name "IDE Controller" --add ide
            vboxmanage storageattach "$vm_name" --storagectl "IDE Controller" --port 0 --device 0 --type dvddrive --medium "$iso_path"
            vboxmanage storageattach "$vm_name" --storagectl "IDE Controller" --port 1 --device 0 --type hdd --medium "$vm_name.vdi"
            ;;
        7)
            echo "Exiting script..."
            exit 0
            ;;
        *)
            echo "Invalid choice. Please try again."
            ;;
    esac
done

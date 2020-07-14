#!/bin/bash
SOURCE_ROOT=./
VENV_DIR_NAME=py3_env
VENV_DIR=$SOURCE_ROOT/$VENV_DIR_NAME

update_apt(){
	apt-get update -y;
	DEBIAN_FRONTEND=noninteractive apt-get upgrade -y;
};

install_req_pkgs(){
	PYTHON_PKGS=(python3-dev python3-pip)
	for i in ${PYTHON_PKGS[@]}; do 
		dpkg --status $i &> /dev/null
		
		if [ $? -eq 0 ]; then
			echo "$i: is Installed!"
		else
			echo "$i: is Not Installed"
			echo "Installing $i ..."
			sudo apt-get install -y $i
		fi
	done
};

create_init_venv_script(){
	unset SCRIPT_NAME
	SCRIPT_NAME=init_python_venv.sh
	cd $SOURCE_ROOT
	
	if [ -f "$SCRIPT_NAME" ]; then
    	echo "Deleting current $SCRIPT_NAME"
    	rm $SCRIPT_NAME
	fi

	printf "#!/bin/bash\n" > $SCRIPT_NAME
	CREATED_SCRIPT="${CREATED_SCRIPT} ${SCRIPT_NAME}"
	printf "## This is a project made within Seoul National University of Science and Technology \n" >> $SCRIPT_NAME
	printf "## Embedded Systems Laboratory 2020 - Raimarius Tolentino Delgado \n\n" >> $SCRIPT_NAME
	printf "## Initiating Python3 Virtual Environment \n\n\n\n" >> $SCRIPT_NAME
	printf "source $VENV_DIR/bin/activate \n" >> $SCRIPT_NAME
}

create_run_script(){
	unset SCRIPT_NAME
	SCRIPT_NAME=sched_test
	MAIN_SCRIPT=main.py
	cd $SOURCE_ROOT

	if [ -f "$SCRIPT_NAME" ]; then
    	echo "Deleting current $SCRIPT_NAME"
    	rm $SCRIPT_NAME
	fi

	printf "#!/bin/bash\n" > $SCRIPT_NAME
	CREATED_SCRIPT="${CREATED_SCRIPT} ${SCRIPT_NAME}"
	printf "## This is a project made within Seoul National University of Science and Technology \n" >> $SCRIPT_NAME
	printf "## Embedded Systems Laboratory 2020 - Raimarius Tolentino Delgado \n\n" >> $SCRIPT_NAME
	printf "## Running the main python script \n\n\n\n" >> $SCRIPT_NAME
	printf "source $VENV_DIR/bin/activate \n" >> $SCRIPT_NAME
	printf "python $MAIN_SCRIPT \n" >> $SCRIPT_NAME

	chmod +x $SCRIPT_NAME
}

create_clean_script(){
	unset SCRIPT_NAME
	SCRIPT_NAME=clean_env.sh
	cd $SOURCE_ROOT

	if [ -f "$SCRIPT_NAME" ]; then
    	echo "Deleting current $SCRIPT_NAME"
    	rm $SCRIPT_NAME
	fi

	printf "#!/bin/bash\n" > $SCRIPT_NAME
	CREATED_SCRIPT="${CREATED_SCRIPT} ${SCRIPT_NAME}"
	printf "## This is a project made within Seoul National University of Science and Technology \n" >> $SCRIPT_NAME
	printf "## Embedded Systems Laboratory 2020 - Raimarius Tolentino Delgado \n\n" >> $SCRIPT_NAME
	printf "## Cleaning python environment \n\n\n\n" >> $SCRIPT_NAME
	printf "rm $CREATED_SCRIPT \n" >> $SCRIPT_NAME
	printf "rm -rf $VENV_DIR \n" >> $SCRIPT_NAME
	printf "rm -rf __pycache__ \n" >> $SCRIPT_NAME
	
	chmod +x $SCRIPT_NAME
}


update_apt;
install_req_pkgs;

mkdir -p $SOURCE_ROOT
sudo -H pip3 install --upgrade pip
sudo -H pip3 install virtualenv
cd $SOURCE_ROOT && virtualenv $VENV_DIR_NAME
source $VENV_DIR/bin/activate

PYTHON_MODS=(pyqt5 numpy)

for i in ${PYTHON_MODS[@]}; do 
	pip install $i
done

create_init_venv_script
create_run_script
create_clean_script
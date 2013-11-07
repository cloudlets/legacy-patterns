# coding: utf-8
# flake8: noqa

import os
from os import path
import yaml

import vagrant
import nepho
#from nepho.core import common, resource
#from nepho.core import  provider
#import nepho.core.provider

NEPHO_VAGRANT_BOILER_PLATE = """#
# Autogenerated by nepho's vagrant provider.
#
# Any changes here will be overwritten.
#
"""


class VagrantProvider(nepho.core.provider.AbstractProvider):
    """An infrastructure provider class for Vagrant"""

    PROVIDER_ID = "vagrant"
    TEMPLATE_FILENAME = "Vagrantfile"

    def initialize_vagrant(self):
        """Creates the desired Vagrantfile in CWD, by rendering a tempalte + context."""

        Vagrantfile_content = self.scenario.get_template()

        try:
            vfile = open("Vagrantfile", "w")
            vfile.write(NEPHO_VAGRANT_BOILER_PLATE)
            vfile.write(Vagrantfile_content)
            vfile.close()
        except IOError:
            print "Error writing out a Vagrantfile in the current directory."
            exit(1)

    def deploy(self):
        """Deploy a given pattern."""
        self.initialize_vagrant()
        v = vagrant.Vagrant()
        try:
            v.up()
        except subprocess.CalledProcessError:
            print "Vagrant exited with non-zero code, but your VM is likely running. Please use the status subcommand to check."

    def status(self):
        v = vagrant.Vagrant()
        status = v.status()
        try:
            status['remote_user'] = v.user()
            status['hostname'] = v.hostname()
            status['port'] = v.port()
            status['keyfile'] = v.keyfile()
            status['conf'] = v.conf()
        except Exception:
            pass
        return status

    def access(self):
        v = vagrant.Vagrant()
        ssh_connect_string = v.user_hostname_port()
        vagrant_binary = vagrant.VAGRANT_EXE
        os.execlp(vagrant_binary, "", "ssh")

    def destroy(self):
        """Bring down a vagrant instance."""
        v = vagrant.Vagrant()
        v.destroy()

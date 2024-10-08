#  test.py
#  afs_server
#
#  Created by Peter Lundkvist on 11/12/2023.
#
#  This is free and unencumbered software released into the public domain.
#  See the file COPYING for more details, or visit <http://unlicense.org>.

import errno
import os

_inserted_disk = None


def initialize():
    pass


def get_inserted_disk():
    global _inserted_disk

    return _inserted_disk


def get_file_list():
    return _file_list


def insert_disk(name):
    global _inserted_disk

    # Eject any inserted disk
    eject_disk()

    # Check if the disk exists
    if (not name in _file_list):
        raise FileNotFoundError(
            errno.ENOENT, os.strerror(errno.ENOENT), name)

    # Save name of disk being inserted
    _inserted_disk = name


def eject_disk():
    global _inserted_disk

    _inserted_disk = None


_file_list = ['Advanced Amiga Analyzer.adf',
              'Alien 3_01_Disk 1.adf',
              'Alien 3_02_Disk 2.adf',
              'Alien Breed - Special Edition 92_01_Disk 1.adf',
              'Alien Breed - Special Edition 92_02_Disk 2.adf',
              'Amiga Test Kit.adf',
              'Beach Volley.adf',
              'Beyond the Ice Palace.adf',
              'California Games_01_Program Disk.adf',
              'California Games_02_Data Disk.adf',
              'Cannon Fodder_01_Disk 1.adf',
              'Cannon Fodder_02_Disk 2.adf',
              'Cannon Fodder_03_Disk 3.adf',
              'Carnage.adf',
              'Carrier Command.adf',
              'Chuck Rock.adf',
              'Cruise for a Corpse_01_Disk 1.adf',
              'Cruise for a Corpse_02_Disk 2.adf',
              'Cruise for a Corpse_03_Disk 3.adf',
              'Cruise for a Corpse_04_Disk 4.adf',
              'Cruise for a Corpse_05_Disk 5.adf',
              'D-Copy.adf',
              'Die Hard 2.adf',
              'Dogs of War.adf',
              'F1.adf',
              'Flood.adf',
              'Gods_01_Disk 1.adf',
              'Gods_02_Disk 2.adf',
              'Gravity Force.adf',
              'Guy Spy_01_Disk 1.adf',
              'Guy Spy_02_Disk 2.adf',
              'Guy Spy_03_Disk 3.adf',
              'Guy Spy_04_Disk 4.adf',
              'Guy Spy_05_Disk 5.adf',
              'Hostages.adf',
              'Hunter.adf',
              'IK+.adf',
              'Indiana Jones and the Fate of Atlantis_01.adf',
              'Indiana Jones and the Fate of Atlantis_02.adf',
              'Indiana Jones and the Fate of Atlantis_03.adf',
              'Indiana Jones and the Fate of Atlantis_04.adf',
              'Indiana Jones and the Fate of Atlantis_05.adf',
              'Indiana Jones and the Fate of Atlantis_06.adf',
              'Indiana Jones and the Fate of Atlantis_07.adf',
              'Indiana Jones and the Fate of Atlantis_08.adf',
              'Indiana Jones and the Fate of Atlantis_09.adf',
              'Indiana Jones and the Fate of Atlantis_10.adf',
              'Indiana Jones and the Fate of Atlantis_11.adf',
              'Indiana Jones and the Fate of Atlantis_Save.adf',
              'Indy Heat.adf',
              'James Pond 2.adf',
              'Jimmy White\'s Whirlwind Snooker.adf',
              'Kick Off 2.adf',
              'Laser Squad.adf',
              'Leatherneck.adf',
              'Lemmings 2 - The Tribes_01_Disk 1.adf',
              'Lemmings 2 - The Tribes_02_Disk 2.adf',
              'Lemmings 2 - The Tribes_03_Disk 3.adf',
              'Lemmings_01_Disk 1.adf',
              'Lemmings_02_Disk 2.adf',
              'Lethal Weapon.adf',
              'Log!cal.adf',
              'Lost Vikings_01_Disk 1.adf',
              'Lost Vikings_02_Disk 2.adf',
              'Lotus Esprit Turbo Challenge.adf',
              'Lotus III - The Ultimate Challenge_01_Disk 1.adf',
              'Lotus III - The Ultimate Challenge_02_Disk 2.adf',
              'Lotus Turbo Challenge 2.adf',
              'Magic Pockets.adf',
              'Miami Chase_01_Disk 1.adf',
              'Miami Chase_02_Disk 2.adf',
              'Micro Machines.adf',
              'Moonstone_01_Disk 1.adf',
              'Moonstone_02_Disk 2.adf',
              'Moonstone_03_Disk 3.adf',
              'North & South.adf',
              'Nuclear War.adf',
              'Oil Imperium_01_Disk 1.adf',
              'Oil Imperium_02_Disk 2.adf',
              'Ooops Up.adf',
              'Pacman 500.adf',
              'Paradroid 90.adf',
              'Pinball Dreams_01_Disk 1.adf',
              'Pinball Dreams_02_Disk 2.adf',
              'Pinball Fantasies_01_Disk 1.adf',
              'Pinball Fantasies_02_Disk 2.adf',
              'Pinball Fantasies_03_Disk 3.adf',
              'Poing.adf',
              'Populous II_01_Disk 1.adf',
              'Populous II_02_Disk 2.adf',
              'Project-X_01_Disk 1.adf',
              'Project-X_02_Disk 2.adf',
              'Project-X_03_Disk 3.adf',
              'Project-X_04_Disk 4.adf',
              'Projectyle.adf',
              'Pushover.adf',
              'Realms_01_Disk 1.adf',
              'Realms_02_Disk 2.adf',
              'Risk.adf',
              'RoboCop 3_01_Disk 1.adf',
              'RoboCop 3_02_Disk 2.adf',
              'RoboCop 3_03_Disk 3.adf',
              'Rocket Ranger_01_Disk 1.adf',
              'Rocket Ranger_02_Disk 2.adf',
              'SWIV.adf',
              'Sensible Soccer_01_Disk 1.adf',
              'Sensible Soccer_02_Disk 2.adf',
              'Sensible Soccer_03_Highlights Disk.adf',
              'Shadow of the Beast III_01_Disk 1.adf',
              'Shadow of the Beast III_02_Disk 2.adf',
              'Silkworm.adf',
              'SimCity.adf',
              'Space Crusade_01_Disk 1.adf',
              'Space Crusade_02_Disk 2.adf',
              'Space Quest II.adf',
              'Space Quest.adf',
              'Speedball 2.adf',
              'Spy vs Spy II.adf',
              'Spy vs Spy III.adf',
              'Spy vs Spy.adf',
              'Starglider 2.adf',
              'Steel Empire_01_Disk 1.adf',
              'Steel Empire_02_Disk 2.adf',
              'Street Fighter II_01_Disk 1.adf',
              'Street Fighter II_02_Disk 2.adf',
              'Street Fighter II_03_Disk 3.adf',
              'Street Fighter II_04_Disk 4.adf',
              'Stunt Car Racer.adf',
              'SysInfo.adf',
              'The Chaos Engine_01_Disk 1.adf',
              'The Chaos Engine_02_Disk 2.adf',
              'The Lost Patrol_01_Disk 1.adf',
              'The Lost Patrol_02_Disk 2.adf',
              'The Settlers_01_Disk 1.adf',
              'The Settlers_02_Disk 2.adf',
              'The Settlers_03_Disk 3.adf',
              'Thundercats.adf',
              'Toki.adf',
              'Troddlers_01_Disk 1.adf',
              'Troddlers_02_Disk 2.adf',
              'Turrican II_01_Disk 1.adf',
              'Turrican II_02_Disk 2.adf',
              'Ugh!.adf',
              'Vixen.adf',
              'Walker_01_Disk 1.adf',
              'Walker_02_Disk 2.adf',
              'Walker_03_Disk 3.adf',
              'Warlords_01_Disk 1.adf',
              'Warlords_02_Disk 2.adf',
              'Warm-Up_01_Disk 1.adf',
              'Warm-Up_02_Disk 2.adf',
              'Wings of Fury.adf',
              'Wizball.adf',
              'Workbench 1.3.adf',
              'Xenon 2 - Megablast_01_Disk 1.adf',
              'Xenon 2 - Megablast_02_Disk 2.adf',
              'Zany Golf.adf',
              '[Demo] Desert Dream (Kefrens)_01_Disk 1.adf',
              '[Demo] Desert Dream (Kefrens)_02_Disk 2.adf',
              '[Demo] Disaster 4 (Packdisk).adf',
              '[Demo] Hardwired (Crionics)_01_Disk 1.adf',
              '[Demo] Hardwired (Crionics)_02_Disk 2.adf',
              '[Demo] Megademo (Phenomena).adf',
              '[Demo] Megademo VIII (Kefrens)_01_Disk 1.adf',
              '[Demo] Megademo VIII (Kefrens)_02_Disk 2.adf',
              '[Demo] Mental Hangover (Scoopex).adf',
              ]

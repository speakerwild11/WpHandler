@echo off
goto :main

:wsl
	<nul set /p ="%~1"|wsl -d Debian
goto :eof

:wp
	call :wsl "wp %~1 --allow-root"
goto :eof


:main	
	wsl --unregister Debian
	wsl --install -d Debian --no-launch
	debian install --root
	call :wsl "cd /etc; echo -e [automount]\\nenabled=false\\n[interop]\\nenabled=false\\n[wsl]\\nidleTimeout=-1 >> wsl.conf; cat wsl.conf"
	wsl -d Debian --shutdown
	call :wsl "apt-get update -y; apt-get upgrade-dist -y"
	call :wsl "apt-get install php -y; apt-get install mariadb-server -y"
	call :wsl "apt-get install php-mysql -y; apt-get install curl -y"
	call :wsl "apt-get install nginx -y; apt-get install php-fpm -y"
	call :wsl "apt-get install daemonize -y; apt-get install syncthing -y"
	call :wsl "cd /etc/nginx/sites-enabled; rm default; curl -O https://raw.githubusercontent.com/speakerwild11/WpHandler/refs/heads/main/default"
	call :wsl "cd /etc/php/8.2/fpm; sed -i \'s|;cgi.fix_pathinfo=1|cgi.fix_pathinfo=0|g\' php.ini"
	call :wsl "curl -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar"
	call :wsl "chmod +x wp-cli.phar; mv wp-cli.phar /usr/local/bin/wp"
	call :wsl "echo create user \'wordpress\'@\'localhost\' identified by \'wordpress\'\; | mariadb"
	call :wsl "echo grant all privileges on wordpress.* to \'wordpress\'@localhost | mariadb"
	call :wsl "echo create database wordpress | mariadb -u wordpress -pwordpress"
	call :wp "core download --path=/var/www/html"
	call :wp "config create --path=/var/www/html --dbhost=localhost --dbname=wordpress --dbuser=wordpress --dbpass=wordpress"
	call :wp "db create --path=/var/www/html"
	call :wp "core install --path=/var/www/html --url=localhost --title=TestServer --admin_name=Administrator --admin_password=placeholder --admin_email=nonsense@doaodaso.com"
	call :wsl "chown -R www-data /var/www/html"
	call :wp "user create Editor 232323@23sa232ssa.com --user_pass=password --role=editor --display_name=Editor --first_name=Editor --last_name=Editor --path=/var/www/html"
	call :wp "user create Author 202dvcxv@iozoc2237.com --user_pass=password --role=author --display_name=Author --first_name=Author --last_name=Author --path=/var/www/html"
	call :wp "user create Contributor 02dasdx@d033.com --user_pass=password --role=contributor --display_name=Contributor --first_name=Contributor --last_name=Contributor --path=/var/www/html"
	call :wp "user create Subscriber dasda@aocxzc.com --user_pass=password --role=subscriber --display_name=Subscriber --first_name=Subscriber --last_name=Subscriber --path=/var/www/html"
	call :wsl "cd /var/www/html; rm index.html; rm index.nginx-debian.html"
	call :wsl "service nginx restart; service php8.2-fpm restart"
	del wordpress_instance
	wsl --export Debian wordpress_instance

	
goto :eofs
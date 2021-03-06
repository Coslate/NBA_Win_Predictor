#! /usr/bin/env python3.6
import pymysql
import re
import random
import datetime
import sys
import argparse
import os

#########################
#     Main-Routine      #
#########################
def main():
    #Initialization
    print('> Crawler Initialization...')
    iter_num = 0
    crawler_nba.init()

    #Argument Parser
    (password, table, max_sql_store_num, unix_socket, database_name) = ArgumentParser()

    #DB Initialization
    print('> DB Initialization...')
    crawler_nba.MySQLDBInitialize(password, table, unix_socket, database_name)

    #Sideband Setting
    current_time = datetime.datetime.now()
    print(f'current_time = {current_time}')
    random.seed(datetime.datetime.now())

    starting_url = "https://en.wikipedia.org/wiki/Kevin_Bacon"
    print(f'starting_url = {starting_url}')

    # Scrape articles from Wikipedia and store into MySQl Database
    choose_link = starting_url
    skipping = 0
    while(iter_num < max_sql_store_num):
        print('iter_num = {}. Get Wiki Links and store the content to MySQL...'.format(iter_num))
        print(f'choose_link = {choose_link}')
        all_internal_links_loop, skipping = crawler_nba.GetWikiLinksContent(choose_link, crawler_nba.cur, table)
        total_num_internal_links_loop = len(all_internal_links_loop)

        if(total_num_internal_links_loop > 0):
            choose_link = "http://en.wikipedia.org"+all_internal_links_loop[random.randint(0, total_num_internal_links_loop-1)].attrs['href']
        if(skipping == 0):
            iter_num += 1

    # Test to read from MySQL Database
    sql_ex = 'SELECT id, title, created, LEFT(content, 32) FROM {table_name} WHERE id=4;'.format(table_name=table)
    crawler_nba.cur.execute(sql_ex)
    results = crawler_nba.cur.fetchall()

    print(f'-------------------Execution {sql_ex}-------------------')
    print(f'table = {table}')
    for row in results:
        id_name = str(row[0])
        title_name = row[1]
        created_name = str(row[2])
        content_name = row[3]

        print('{x:<2s}, {y:<2s}, {z:<2s}, {k:<2s}'.format(x=id_name, y=title_name, z=created_name, k=content_name))

    # Close the connection of MySQL Database
    crawler_nba.MySQLDBClose(crawler_nba.cur, crawler_nba.conn)
#########################
#     Sub-Routine       #
#########################
def ArgumentParser():
    password      = ""
    table         = ""
    database_name = ""
    unix_socket = ""
    max_sql_store_num = 10

    parser = argparse.ArgumentParser()
    parser.add_argument("--mysql_password", "-sql_p", help="The password to connect to MySQL server.", required=True)
    parser.add_argument("--mysql_table_name", "-sql_tn", help="The table name that will be used to store data.", required=True)
    parser.add_argument("--max_sql_store_num", "-sql_mx_sn", help="The maximum number that stores in MySQL table.", required=True)
    parser.add_argument("--unix_socket", "-sql_un_sock", help="The unix_socket that is used to mypysql connection.", required=True)
    parser.add_argument("--database_name", "-database_name", help="The unix_socket that is used to mypysql connection.", required=True)

    args = parser.parse_args()

    if args.mysql_password:
        password = args.mysql_password
    if args.mysql_table_name:
        table = args.mysql_table_name
    if args.max_sql_store_num:
        max_sql_store_num = int(args.max_sql_store_num)
    if args.unix_socket:
        unix_socket = args.unix_socket
    if args.database_name:
        database_name = args.database_name

    return(password, table, max_sql_store_num, unix_socket, database_name)

#-----------------Execution------------------#
if __name__ == '__main__':
    import sys
    this_script_path = os.path.realpath(__file__)
    this_script_folder = os.path.dirname(this_script_path)
    crawler_nba_pkg_path = this_script_folder+'/../../crawler'
    print('Add to sys.path : {x}'.format(x=crawler_nba_pkg_path))
    sys.path.append(crawler_nba_pkg_path)
    import package_crawler_nba.crawler_nba as crawler_nba
    print('Import package_crawler_nba successfully.')

    main()

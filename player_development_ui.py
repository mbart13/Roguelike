from colored import fg, attr
BLUE = fg('blue')
RES = attr('reset')


class AdvanceScreenController():
    indent_price = 20

    def display_screen(self, developer_data):
        if developer_data.first_time:
            print(f'{BLUE}Prepare for your journey.')
            print(f'Points to spend: {developer_data.points_to_spend}\n')
        else:
            print(f'{BLUE}You have died. Nice try!')
            print(f'Old rank: {developer_data.old_player.advancement["rank"]}    New rank: {developer_data.new_rank}  Points to spend: {developer_data.points_to_spend}\n')

        print(f"      Max HP: {developer_data.new_stats.status['hp']['max_base']}"+f"\033[4;{self.indent_price}H"+f" Price: {(developer_data.new_stats.status['hp']['advances']+1)}")
        print(f"      Damage: {developer_data.new_stats.attributes['damage']['base']}"+f"\033[5;{self.indent_price}H"+f" Price: {(developer_data.new_stats.attributes['damage']['advances']+1)*developer_data.attributes_list[0][2]}")
        print(f"      Attack: {developer_data.new_stats.attributes['attack']['base']}"+f"\033[6;{self.indent_price}H"+f" Price: {(developer_data.new_stats.attributes['attack']['advances']+1)*developer_data.attributes_list[1][2]}")
        print(f"      Armor: {developer_data.new_stats.attributes['armor']['base']}"+f"\033[7;{self.indent_price}H"+f" Price: {(developer_data.new_stats.attributes['armor']['advances']+1)*developer_data.attributes_list[2][2]}")
        print(f"      Defense: {developer_data.new_stats.attributes['defense']['base']}"+f"\033[8;{self.indent_price}H"+f" Price: {(developer_data.new_stats.attributes['defense']['advances']+1)*developer_data.attributes_list[3][2]}")
        print(f"      Perception: {developer_data.new_stats.attributes['perception']['base']}"+f"\033[9;{self.indent_price}H"+f" Price: {(developer_data.new_stats.attributes['perception']['advances']+1)*developer_data.attributes_list[4][2]}")
        print(f"      Charisma: {developer_data.new_stats.attributes['charisma']['base']}"+f"\033[10;{self.indent_price}H"+f" Price: {(developer_data.new_stats.attributes['charisma']['advances']+1)*developer_data.attributes_list[5][2]}\n")
        print(f"Press 'w' and 's' to choose a stat, 'd' to increase it.")
        print(f"Press 'F' to finish.")
        print(f"\033[{developer_data.selector};0H", end='')
        print(f'---->')

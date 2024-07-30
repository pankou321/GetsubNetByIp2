#pip install ipwhois
#
#blackipsin.txt
#/*ipaddress,countryName*/
#170.239.86.172,Chile
#177.221.141.83,Chile
#186.173.8.157,Chile
#186.189.85.255,Chile
#
#
# python .\GetsubNetByIp.py


from ipwhois import IPWhois
import ipaddress

def get_ip_info(ip):
    try:
        obj = IPWhois(ip)
        results = obj.lookup_rdap()
        
        # 提取网络信息
        network_info = results.get('network', {})
        cidr = network_info.get('cidr', 'N/A')
        if cidr != 'N/A':
            network = ipaddress.ip_network(cidr, strict=False)
            start_address = network.network_address
            end_address = network.broadcast_address
            cidr = str(network)
        else:
            start_address = end_address = 'N/A'

        return {
            'start_address': str(start_address),
            'end_address': str(end_address),
            'cidr': cidr
        }
    except Exception as e:
        print(f"Error fetching information for {ip}: {e}")
        return {'start_address': 'Error', 'end_address': 'Error', 'cidr': 'Error'}

def process_ips(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            parts = line.strip().split(',')
            ip = parts[0].strip()
            annotation = parts[1].strip() if len(parts) > 1 else 'N/A'
            
            network_info = get_ip_info(ip)
            
            # 写入结果到输出文件
            outfile.write(f"IP Address: {ip},{annotation}\n")
            outfile.write(f"start_address: {network_info['start_address']}\n")
            outfile.write(f"end_address: {network_info['end_address']}\n")
            outfile.write(f"cidr: {network_info['cidr']}\n")
            outfile.write("\n")  # 添加空行分隔不同 IP 的结果

if __name__ == "__main__":
    input_file = 'blackipsin.txt'
    output_file = 'blackipout.txt'
    process_ips(input_file, output_file)


<table>
                <thead>
                    <tr>
                        <td>Host name</td>
                        <td>Requests</td>
                    </tr>
                </thead>
                <tbody>
% for host in hosts:
                    <tr>
                        <td><a href="/hosts/sessions/${host['host']}" class=".hostCount" data-type="host_count" data-host="${host['host']}" >${host['host']}</a></td>
                        <td>${host['count']}</td>
                    </tr>
% endfor
                </tbody>
            </table>
            
<script>
    //Ghetto as all hell
    ts = ${ts}
</script>
<span>
    <a href="/">Host List</a> >> <a href="/hosts/sessions/${host}">${host}</a>  
</span>
<h2>Session digest for ${host}</h2>

<table>
    <thead>    
        <tr>
            <th>URI</th>
            <th>Type</th>
        </tr>
    </thead>
    <tbody>
% for uri in uris:
        <tr>
            <td><a href="/hosts/uri/${host}/${uri|u}/">${uri}</a></td>
            <td>${getContentTypes(uri)}</td>
        </tr>
% endfor
    </tbody>
</table>

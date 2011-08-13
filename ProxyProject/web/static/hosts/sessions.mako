<h2>Session digest for ${host}</h2>

<div>
    <ul>
    % for uri in uris:
    <li><a href="/hosts/uri/${host}/${uri|u}/">${uri}</a></li>
    % endfor
    </ul>
</div>

<span>
    <a href="/">Host List</a> >> <a href="/hosts/sessions/${host}">${host}</a>   
</span>


%for record in uris:
<h2>Record</h2>
<fieldset>
    <legend>Request</legend>
    <h3>Headers</h3>
    <table>
    % for name, value in record.request['headers'].items():
        <tr>
            <td>${name}</td>
            <td>${value|h}</td>
        </tr>        
    % endfor
    </table>
</fieldset>
<fieldset>
    <legend>Response</legend> 
    <h3>Headers</h3>
    <table>
    % for name, value in record.response['headers'].items():
        <tr>
            <td>${name}</td>
            <td>${value|h}</td>
        </tr>        
    % endfor
    </table>    
</fieldset>

% endfor


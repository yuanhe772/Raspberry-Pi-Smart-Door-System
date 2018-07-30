var dynamicTable = (function() {
    var _tableId, _table, _fields, _headers, _defaultText;
    
    function _buildRowColumns(names, item){
        var row = '<tr>';
        if (names && names.length > 0){
            $.each(names, function(index, name){
                var c = item ? item[name+''] : name;
                row += '<td>' + c + '</td>';
            });
        }
        row += '</tr>';
        return row;
    }
    
    function _buildHeaderRow(names, item){
        var row = '<tr>';
        if (names && names.length > 0){
            $.each(names, function(index, name){
                var c = item ? item[name+''] : name;
                row += '<th>' + c + '</th>';
            });
        }
        row += '</tr>';
        return row;
    }
    
    function _setHeaders() {
        _headers = (_headers == null || _headers.length < 1) ? _fields : _headers;
        var h = _buildHeaderRow(_headers);
        if (_table.children('thead').length < 1) _table.prepend('<thead></thead>');
        _table.children('thead').html(h);
    }
    
    function _setNoItemsInfo() {
        if (_table.length < 1) return; // not configured
        var colspan = _headers != null && _headers.length > 0 ? 'colspan="'+_headers.length+'"' : '';
        var content = '<tr class="no-items"><td ' + colspan + 'style="text-align:center">' + _defaultText + '</td></tr>';
        if (_table.children('tbody').length > 0) _table.children('tbody').html(content);
        else _table.append('<tbody>' + content + '</tbody>');
    }
    
    function _removeNoItemsInfo() {
        var c = _table.children('tbody').children('tr');
        if (c.length == 1 && c.hasClass('no-items')) _table.children('tbody').empty();
    }
    
    return {
        config: function(tableId, fields, headers, defaultText) {
            _tableId = tableId;
            _table = $('#'+tableId);
            _fields = fields || null;
            _headers = headers || null;
            _defaultText = defaultText || 'No items in this list...';
            _setHeaders();
            _setNoItemsInfo();
            return this;
        },
        load: function(data, append){
            if (_table.length < 1) return; // not conf'd
            _setHeaders();
            _removeNoItemsInfo();
            if (data && data.length>0){
                var rows = '';
                $.each(data, function(index, item){
                    rows += _buildRowColumns(_fields, item); 
                });
                var mthd = append ? 'append' : 'html';
                _table.children('tbody')[mthd](rows);
            } else {
                _setNoItemsInfo();
            }
            return this;
        },
        clear: function() {
            _setNoItemsInfo();
            return this;
        }
    };
} ());
def calculate_portfolio_stats(portfolio):
    total_value = sum(stock.current_value for stock in portfolio.stocks)
    total_cost = sum(stock.shares * stock.purchase_price for stock in portfolio.stocks)
    total_gain_loss = total_value - total_cost
    total_gain_loss_percentage = (total_gain_loss / total_cost * 100) if total_cost > 0 else 0
    
    return {
        'total_value': total_value,
        'total_cost': total_cost,
        'total_gain_loss': total_gain_loss,
        'total_gain_loss_percentage': total_gain_loss_percentage,
        'num_positions': len(portfolio.stocks)
    }
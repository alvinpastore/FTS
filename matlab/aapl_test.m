close all;

closing_prices = aapl(:,5);
previous_price = 0;
count_hi = 0;
count_lo = 0;
amount = 10;
budget = 100000;
shares = 0;
vector_idx = 0;

budget_vector = zeros(length(closing_prices),1);
buy_sell_vector = zeros(length(closing_prices),1);
holdings_vector = zeros(length(closing_prices),1);

for t = 1:length(closing_prices)
    vector_idx = vector_idx + 1;
    price = closing_prices(t);
    total = amount * price;
    
    if price > previous_price
        count_hi = count_hi + 1;
        if count_hi >= 3
            %BUY, update budget and reset count_high
            shares = shares + amount;
            buy_sell_vector(vector_idx) = 1;
            holdings_vector(vector_idx) = total;
            budget = budget - total;
            count_hi = 0;
        end
        
    elseif price < previous_price
        count_lo = count_lo + 1;
        if count_lo >= 3
            %SELL, update budget and reset count_low
            shares = shares - amount;
            buy_sell_vector(vector_idx) = -1;
            budget = budget + total;
            holdings_vector(vector_idx) = -total;
            count_lo = 0;
        end
    end
    budget_vector(vector_idx) = budget;
    previous_price = price;
end
if shares
    budget = budget + (shares * price);
end
hold on
plot(1:length(closing_prices), closing_prices*1000,'b-');
plot(1:length(closing_prices),budget_vector,'g-');
plot(1:length(closing_prices),budget_vector+holdings_vector,'r-');


hold off;
%figure();
%plot(1:length(closing_prices),holdings_vector,'k-');


%figure();
%plot(1:length(closing_prices),buy_sell_vector,'rx');


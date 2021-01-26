from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import OrdinalEncoder


class AccutuningIntegerEncode(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.oe = OrdinalEncoder()
        self.columns_to_encode = list()

    def fit(self, X, y=0, **fit_params):
        self.columns_to_encode = list(
            X.select_dtypes(include=['object'])
        )

        for col in self.columns_to_encode:
            # Null 값이 있으면 encoder에서 에러 발생한다. (추후 수정 필요)
            # integer(float) or 'NaN'이 섞여있어도 에러 발생한다.
            X.loc[:, col] = X.loc[:, col].fillna('NaN').apply(str)

        try:
            self.oe.fit(X.loc[:, self.columns_to_encode])
        except Exception as e:
            print(self.columns_to_encode)
            print(e)
            raise
        return self

    def transform(self, X, y=0):
        X_tr = X.copy()
        for col in self.columns_to_encode:
            X_tr.loc[:, col] = X.loc[:, col].fillna('NaN').apply(str)
        X_tr.loc[:, self.columns_to_encode] = self.oe.transform(X_tr.loc[:, self.columns_to_encode])
        return X_tr
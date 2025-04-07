# Modelling workflow

###  <ins> 1. ModelSelection.ipynb  </ins>
Tests the performance of a number of different machine learning models using 10-fold cross validation. These include:
* Linear regression
* Random Forest
* XGBoost
* Extra Trees Regressor

The outputs of the 10-fold cross validation process are:
* The error metric scores associated with that model (averaged over all folds)
    * The MAE, the MAPE and the RMSE
### <b> Conclusion: Random Forest Regressor is best performing model </b>

There was another version of this script where Year was not included as a variable (this is now deleted as decided it shouldn't be included)

###  <ins> 2. ModelSelection_TestBufferSize.ipynb </ins>
Tests the performance of a random forest regressor using features collected within a number of different buffer sizes: 50,100,200,300,400,500,600,1000

The outputs of the 10-fold cross validation process are:
* The error metric scores associated with that model (averaged over all folds)
    * The MAE, the MAPE and the RMSE

<b> Conclusion: 400-500m buffer results in best performing model </b>

###  <ins> 3. ModelEvaluation.ipynb  </ins>
Tests the performance of a random forest regressor using features collected within 400m.

This is validated using a simple 80 - 20 train test split with the chronological order of the data preserved.  
The outputs of the validation process are:
* The error metric scores associated with that model (averaged over all folds)
    * The MAE, the MAPE and the RMSE
* The Gini feature importance associated with each fold
* The model used in each fold, from which the permutation imporance associated with each fold can be calculated
* A prediction for each data point in the dataset (within cross validation each data point is included in the test set only once and thus despite their beng multiple cross-validation folds, each true value of Y has only one associated prediction )

Also breaks down prediction and prediction error by different time slices and different parts of city. 

###  <ins> 4. FittingFinalModel.ipynb </ins>
Fit a Random Forest Regressor with a 500m buffer on the whole dataset. Saves this model to a pickle file so it can be reused in future. Also saves the predictor variables used in constructing it, and the real values associated with those predictor variables.

###  <ins> 5. AssessingFinalmodel.ipynb  </ins>
Reads in the Random Forest model fitted on the whole dataset from the pickle file. 
Find the Gini and Permutation feature importances returned from this final fitted model.  
There are no predicted values to plot, because we fitted the model on the whole dataset.

###  <ins> 6. UsingModelToEvaluateEvents.ipynb  </ins>

Evalues the model on a few key events to see how well it is able to quantify the change in footfall that
would have otherwise been predicted on those days.

###  <ins> 7(a/b). TestingFinalModel.ipynb  </ins>

Two scripts that look at how well the model peforms on a single post-covid dataset (a) and 
how well it performs on a few different post-covid time periods.


